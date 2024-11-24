import fire

from run import evaluate


def _eval_domain(domain, model_name, model_checkpoint_path, model_dtype):

    for label_noise in ["factual", "nonfactual", "empty_def", "ood", "ood_empty_def"]:
        kwargs = dict(
            model_name=model_name,
            domain=domain,
            source_key="text",
            guidelines=["definition"],
            seed=17,
            shuffle=True,
            balanced=True,
            output_dir="output",
            use_model_cache=True,
        )
        if domain == "financial":
            kwargs["concept"] = "capital"
            kwargs["target_key"] = "capital"
            kwargs["label_type"] = "concept"
            kwargs["max_samples"] = 540
            kwargs["dataset_name"] = "data/financial_reports.csv"
        elif domain == "scientific":
            kwargs["concept"] = "llm_definitions"
            kwargs["target_key"] = "coarse_concept"
            kwargs["max_samples"] = 500
            kwargs["dataset_name"] = "data/artcorpus_sample.csv"
        else:
            raise ValueError(f"Unsupported domain: {domain}")

        if label_noise in ["nonfactual", "ood"]:
            kwargs["label_noise"] = label_noise
        if "empty_def" in label_noise:
            kwargs["empty_definition"] = True
        if model_checkpoint_path:
            kwargs["model_checkpoint_path"] = model_checkpoint_path
        if model_dtype:
            kwargs["model_dtype"] = model_dtype

        evaluate(**kwargs)


def main(
    model_name="gpt-4-0613",
    domain=None,
    model_checkpoint_path=None,
    model_dtype=None,
):
    if domain is None:
        domains = ["financial", "scientific"]
    elif isinstance(domain, str):
        domains = [domain]
    else:
        domains = domain

    for domain in domains:
        _eval_domain(domain, model_name, model_checkpoint_path, model_dtype)


if __name__ == "__main__":
    fire.Fire(main)
