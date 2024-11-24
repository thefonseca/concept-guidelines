from glob import glob

import fire
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt


def get_guideline_effects(paths):
    results = {}
    for path in paths:
        data = pd.read_csv(path)
        for col in data.columns:
            if "guideline_match_" in col:
                col_data = data[col].dropna()
                results[f"{col}_avg"] = col_data.mean()

                total_count = 0
                for val, effect in [(1, "positive"), (-1, "negative"), (0, "neutral")]:
                    col_count = sum(col_data == val)
                    count = results.get(f"{col}_{effect}", 0)
                    count += col_count
                    results[f"{col}_{effect}"] = count
                    total_count += count

                for effect in ["positive", "negative", "neutral"]:
                    count = results[f"{col}_{effect}"]
                    results[f"{col}_{effect}_norm"] = count / total_count

    return results


def plot_effects(paths, domain, effect="positive"):
    guideline_effects = get_guideline_effects(paths)
    effects = []
    for key in sorted(guideline_effects):
        if f"{effect}_norm" in key:
            key_ = key.replace("guideline_match_", "")
            key_ = key_.replace(f"_{effect}_norm", "")
            key_ = key_.replace("Social and relationship", "Social & Rel.")
            col_a, col_b = key_.split("_")
            effects.append(
                {
                    "concept_a": col_a,
                    "concept_b": col_b,
                    "accuracy": guideline_effects[key],
                }
            )

    df = pd.DataFrame(effects)
    df = df.pivot(index="concept_a", columns="concept_b", values="accuracy")
    # specify size of heatmap
    # fig, ax = plt.subplots(figsize=(10, 4.5))
    sns.set_theme(style="white", font="freeserif", font_scale=1.4)
    chart = sns.heatmap(df, annot=True, cmap="Blues", fmt=".1g")
    chart.set_xticklabels(
        chart.get_xticklabels(), rotation=45, horizontalalignment="right"
    )
    # chart.set_ylabel('Llama-2-7B', fontdict={'weight': 'bold'})
    plt.savefig(f"guideline_effects_{domain}.pdf", bbox_inches="tight")
    plt.clf()
    return df


def main():
    metric_paths = {
        "financial_llama2": "data/results/financial/reports_sample_eacl_20231013*llama-2-7b-chat-financial*/*metrics_per_sample.csv",
        "financial_gpt": "data/results/financial/reports_sample_eacl_20231013*gpt-3.5-*-financial*/*metrics_per_sample.csv",
        "scientific_llama2": "data/results/scientific/train_*llama-2-7b-chat-scientific-chatgpt_random-definition*/*metrics_per_sample.csv",
        "scientific_gpt": "data/results/scientific/train_*gpt-3.5*-scientific-chatgpt_random-definition*/*metrics_per_sample.csv",
    }

    for domain_model, metric_path in metric_paths.items():
        paths = glob(metric_path)
        _ = plot_effects(paths, domain_model)


if __name__ == "__main__":
    fire.Fire(main)
