import fire
import itertools
import logging
from pathlib import Path
from pprint import pformat
import random

import pandas as pd

from llms.classifiers.evaluation import evaluate_classifier

from guidelines.financial import GUIDELINES as financial_guidelines
from guidelines.scientific import GUIDELINES as scientific_guidelines

from llms.metrics import rouge_score
from llms.utils.utils import config_logging

logger = logging.getLogger(__name__)

GUIDELINES = {"financial": financial_guidelines, "scientific": scientific_guidelines}

OOD_LABELS = [
    "Flibberknock",
    "Quibblesnatch",
    "Blibberflop",
    "Ziggledorf",
    "Snizzlewump",
    "Wobblequark",
    "Jibberplunk",
    "Crumblefluff",
    "Splonglewort",
    "Dinglewhack",
]


def _get_run_id(
    model_name, domain, concept, guideline_keys, label_noise_type, n_label_samples, idx
):
    label_noise_str = ""
    if label_noise_type:
        label_noise_str = f"{label_noise_type}-"

    count_str = ""
    if n_label_samples > 1:
        count_str = f"_{idx}_of_{n_label_samples}"

    run_id = f"{model_name}-{domain}-{concept}_{label_noise_str}{'-'.join(guideline_keys)}{count_str}"
    return run_id


def _get_example_guidelines(
    guideline,
    label_permutation,
    examples_per_label,
    label_type,
    noisy_channel,
    random_,
):
    examples = []
    for label, original_label in label_permutation.items():
        if original_label:
            label_examples = list(guideline[original_label])
        else:
            label_examples = [""]
        random_.shuffle(label_examples)
        label_examples = label_examples[:examples_per_label]
        if noisy_channel:
            label_examples = [f"{label}: {x}" for x in label_examples]
        else:
            label_examples = [
                f"Text: {x}\n{label_type}: {label}" for x in label_examples
            ]
        examples.extend(label_examples)
    return examples


def get_context_prompt(
    guidelines,
    guideline_keys,
    label_permutation,
    examples_per_label,
    label_type,
    empty_definition,
    add_task_prompt,
    add_previous_text,
    noisy_channel,
    random_,
):
    context_prompt = []
    guideline_prompt = guidelines.get("guideline_prompt")

    if guideline_keys:
        for g_key in guideline_keys:
            guideline = guidelines[g_key]

            if g_key == "examples":
                g_item = _get_example_guidelines(
                    guideline,
                    label_permutation,
                    examples_per_label,
                    label_type,
                    noisy_channel,
                    random_,
                )
                g_item = "\n\n".join(g_item)

            elif g_key == "definition":
                if empty_definition:
                    g_item = [f"- {l}" for l in label_permutation]
                else:
                    g_item = [
                        f"- {k}: {guideline[v]}" if v else f"- {k}"
                        for k, v in label_permutation.items()
                    ]
                random_.shuffle(g_item)
                if add_task_prompt:
                    if guideline_prompt:
                        g_item = [guideline_prompt] + g_item
                g_item = "\n\n".join(g_item)

            context_prompt.append(g_item)

        if add_task_prompt and "definition" in guideline_keys:
            task_prompt = (
                "Classify the text below into one of the categories listed above."
                "\nBe concise and write only the category name."
            )
            context_prompt.append(task_prompt)

        if add_previous_text:
            context_prompt.append("Previous text: {previous_text}")

        context_prompt = "\n\n".join(context_prompt)

    if len(context_prompt) == 0:
        context_prompt = None

    return context_prompt


def get_permutation_similarity(label_permutation, definitions, type=None):
    similarity = 0
    for label_a, label_b in label_permutation.items():
        if type and "rouge" in type:
            score = rouge_score(
                definitions[label_a], definitions[label_b], rouge_ngrams=[type]
            )
            score = score[type].fmeasure
        else:
            score = int(label_a == label_b)
        similarity += score
    similarity /= len(label_permutation)
    return similarity


def get_label_permutation(
    labels, label_noise_type, random_, permutation_idx=0, shuffle=False
):
    label_permutation = {}
    if label_noise_type and label_noise_type == "nonfactual":
        # 'nonfactual' is a random total permutation
        labels_shuffled = []
        for label in labels:
            other_labels = [
                l for l in labels if l != label and l not in labels_shuffled
            ]
            random_label = random_.choice(other_labels)
            labels_shuffled.append(random_label)
            label_permutation[random_label] = label

    elif label_noise_type and label_noise_type == "ood":
        # out-of-dictionary (OOD) labels
        ood_labels_list = []
        for label in labels:
            other_labels = [l for l in OOD_LABELS if l not in ood_labels_list]
            ood_label = random_.choice(other_labels)
            ood_labels_list.append(ood_label)
            label_permutation[ood_label] = label
    else:
        label_permutation = {l: l for l in labels}

    if shuffle and random_:
        label_permutations = list(
            itertools.permutations(list(label_permutation.keys()))
        )
        if permutation_idx < len(label_permutations):
            random_.shuffle(label_permutations)
            shuffled_keys = label_permutations[permutation_idx]

            if label_noise_type and label_noise_type == "random":
                values = label_permutation.values()
                label_permutation = {k: v for k, v in zip(shuffled_keys, values)}
            else:
                label_permutation = {k: label_permutation[k] for k in shuffled_keys}

    return label_permutation


def sample_balanced(sources, targets, max_samples=None, random_state=17, logger=None):
    def is_empty(x):
        return x is None or str(x) == "nan"  # or x == 'Other'

    empty_target_idxs = [ii for ii in range(len(targets)) if is_empty(targets[ii])]
    targets = [targets[ii] for ii in range(len(targets)) if ii not in empty_target_idxs]
    sources = [sources[ii] for ii in range(len(sources)) if ii not in empty_target_idxs]

    classes = sorted(set(targets))
    targets_pd = pd.Series(targets)

    if max_samples:
        max_per_class = max_samples // len(classes)
    else:
        max_per_class = targets_pd.value_counts().min()

    if logger:
        logger.info(
            f"Sampling balanced data for {len(classes)} classes"
            f" (maximum of {max_per_class} samples per class; seed={random_state})"
        )
    idxs = []
    for class_ in classes:
        class_targets = targets_pd[targets_pd == class_]
        n_samples = min(len(class_targets), max_per_class)
        class_samples = class_targets.sample(n_samples, random_state=random_state)
        idxs.extend(class_samples.index.values.tolist())
        if logger:
            logger.info(f'Added {len(class_samples)} samples for class "{class_}"')

    sources = [sources[idx] for idx in idxs]
    targets = [targets[idx] for idx in idxs]
    return sources, targets


def add_permutation_metrics(label_permutation, definitions, metrics):
    new_metrics = {}
    for metric in ["edit", "rouge1", "rouge2"]:
        similarity = get_permutation_similarity(
            label_permutation, definitions, type=metric
        )
        scores = metrics.get(f"permutation_{metric}_distance", [])
        scores = list(scores)
        scores.append(1 - similarity)
        new_metrics[f"permutation_{metric}_distance"] = scores
    return new_metrics


def guideline_effect(
    prediction,
    reference=None,
    source=None,
    label_permutation=None,
    factual_prediction_fn=None,
    parallelized=False,
    index=None,
    **kwargs,
):
    factual_prediction = factual_prediction_fn(index)
    label_permutation = {v: k for k, v in label_permutation.items()}
    metrics = {f"guideline_match_{k}_{v}": None for k, v in label_permutation.items()}
    score = None
    if factual_prediction not in label_permutation:
        if factual_prediction == "Objective":
            factual_prediction = "Motivation"
        else:
            factual_prediction = "[OOV_LABEL]"

    if prediction not in label_permutation:
        if prediction == "Objective":
            prediction = "Motivation"
        else:
            prediction = "[OOV_LABEL]"

    if factual_prediction not in label_permutation:
        if prediction == factual_prediction:
            score = 0
    else:
        expected_label = label_permutation[factual_prediction]
        if expected_label == prediction:
            score = 1
        elif prediction == factual_prediction:
            score = 0
        else:
            score = -1

        metrics[f"guideline_match_{factual_prediction}_{expected_label}"] = score

    metrics["guideline_match"] = score
    return metrics


def evaluate(
    concept="capital",
    domain="financial",
    guidelines=None,
    examples_per_label=1,
    label_noise=None,
    n_permutations=1,
    balanced=False,
    empty_definition=False,
    n_permutations_per_distance=None,
    add_task_prompt=True,
    label_type=None,
    measure_guideline_effect=False,
    shuffle_guidelines=False,
    run_id=None,
    model_name=None,
    source_key="text",
    seed=17,
    **kwargs,
):
    random_ = random.Random(seed)
    concept_guidelines = GUIDELINES[domain][concept]
    guideline_keys = guidelines
    if label_type is None:
        label_type = f"{domain} concept".capitalize()
    noisy_channel = kwargs.get("model_noisy_channel", False)
    labels = concept_guidelines.get("labels")
    add_previous_text = isinstance(source_key, dict) and "previous_text" in source_key
    param_dict = dict(
        concept=concept,
        domain=domain,
        guidelines=guidelines,
        label_noise=label_noise,
        empty_definition=empty_definition,
        examples_per_label=examples_per_label,
        n_permutations=n_permutations,
        add_task_prompt=add_task_prompt,
        add_previous_text=add_previous_text,
        balanced=balanced,
        source_key=source_key,
        seed=seed,
    )

    if labels is None:
        labels = sorted(list(concept_guidelines["definition"].keys()))

    if isinstance(labels, list):
        labels = {l: l for l in labels}

    preprocess_fn = None
    if balanced:
        preprocess_fn = lambda sources, targets, **kwargs: sample_balanced(
            sources, targets, random_state=seed, **kwargs
        )

    target_key = kwargs.pop("target_key", concept)
    accuracies = []
    output_path = None
    permutation_metric_counts = {}
    permutation_metrics = {}
    idx = 0
    last_run_count = 0
    factual_result = None

    while len(accuracies) < n_permutations:
        run_factual_guidelines = (
            label_noise in ["random", "nonfactual"]
            and measure_guideline_effect
            and factual_result is None
        )
        permutation_idx = len(accuracies) + (not run_factual_guidelines)

        if (
            run_id is None and len(accuracies) != last_run_count
        ) or last_run_count == 0:
            run_id_ = _get_run_id(
                model_name,
                domain,
                concept,
                guideline_keys,
                label_noise,
                n_permutations,
                permutation_idx,
            )
            timestr = config_logging(run_id=run_id_, **kwargs)
        elif run_id:
            run_id_ = run_id
            timestr = config_logging(run_id=run_id_, **kwargs)

        last_run_count = len(accuracies)

        if run_factual_guidelines:
            label_permutation = get_label_permutation(
                labels, None, None, shuffle=shuffle_guidelines
            )

        elif label_noise == "random":
            label_permutation = get_label_permutation(
                labels,
                label_noise,
                random.Random(seed),
                permutation_idx=idx,
                shuffle=shuffle_guidelines,
            )
        else:
            label_permutation = get_label_permutation(
                labels, label_noise, random_, shuffle=shuffle_guidelines
            )

        if label_permutation is None or len(label_permutation) == 0:
            logger.info(f"No permutations remaining. Exiting loop.")
            break

        guideline_metrics = None
        if not run_factual_guidelines and label_noise in ["random", "nonfactual"]:
            permutation_metrics_tmp = add_permutation_metrics(
                label_permutation, concept_guidelines["definition"], permutation_metrics
            )
            distance = permutation_metrics_tmp[f"permutation_edit_distance"][-1]
            distance_count = permutation_metric_counts.get(distance, 0)

            if n_permutations_per_distance:
                if distance_count >= n_permutations_per_distance:
                    idx += 1
                    continue

            permutation_metrics = permutation_metrics_tmp
            permutation_metric_counts[distance] = distance_count + 1

            if factual_result:
                factual_prediction_fn = lambda index: factual_result["predictions"][
                    index
                ]
                guideline_metrics = [
                    dict(
                        metric_fn=guideline_effect,
                        metric_kwargs=dict(
                            label_permutation=label_permutation,
                            factual_prediction_fn=factual_prediction_fn,
                        ),
                    )
                ]

        labels_ = labels
        if label_noise and label_noise == "ood":
            labels_ = {k: labels[v] for k, v in label_permutation.items()}

        logger.info(
            f"Processing label permutation {permutation_idx} of {n_permutations}:\n{pformat(label_permutation)}"
        )
        logger.info(f"Parameters:\n{pformat(param_dict)}")

        context_prompt = get_context_prompt(
            concept_guidelines,
            guideline_keys,
            label_permutation,
            examples_per_label,
            label_type,
            empty_definition,
            add_task_prompt,
            add_previous_text,
            noisy_channel,
            random_,
        )
        logger.info(f"context_prompt:\n\n{context_prompt}")

        result = evaluate_classifier(
            model_name=model_name,
            model_context_prompt=context_prompt,
            model_labels=labels_,
            model_label_type=label_type,
            source_key=source_key,
            target_key=target_key,
            preprocess_fn=preprocess_fn,
            metrics=guideline_metrics,
            timestr=timestr,
            run_id=run_id_,
            seed=seed,
            **kwargs,
        )
        if output_path is None:
            output_path = result["output_path"]

        if run_factual_guidelines:
            factual_result = result
            random_ = random.Random(seed)
        else:
            agg_scores = result["agg_scores"]
            accuracies.append(
                agg_scores["classification_metrics"]["exact_match"]["mean"]
            )
            idx += 1

    permutation_metrics["accuracy"] = accuracies
    logger.debug(f"Permutation metrics:\n{pformat(permutation_metrics)}")
    permutation_metrics = pd.DataFrame(permutation_metrics)

    if n_permutations > 1:
        corr = permutation_metrics.corr()
        for metric in permutation_metrics:
            if metric == "accuracy":
                continue
            logger.info(f"Correlation with {metric}:\n{corr.loc[metric]}")
        logger.info(f"Permutation metric counts:\n{pformat(permutation_metric_counts)}")

    if output_path:
        file_path = Path(output_path).parent / "permutation_metrics.csv"
        permutation_metrics.to_csv(file_path, index=False)


if __name__ == "__main__":
    fire.Fire(evaluate)
