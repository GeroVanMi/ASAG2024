import pandas as pd
from datasets import load_dataset


def transform_dataset_to_dataframe_with_split_name(
    split_dataset, split_name
) -> pd.DataFrame:
    df = split_dataset.to_pandas()
    df["split"] = split_name
    return df


def load_saf_huggingface_splits():
    return load_dataset("Short-Answer-Feedback/saf_communication_networks_english")


def load_saf():
    saf_datasets = load_saf_huggingface_splits()
    splits = [
        transform_dataset_to_dataframe_with_split_name(saf_datasets[key], key)
        for key in saf_datasets
    ]
    combined_splits = pd.concat(splits)
    filtered = combined_splits[combined_splits["score"] <= 1]
    return filtered.copy()


def rename_saf(saf: pd.DataFrame) -> pd.DataFrame:
    return saf.rename(
        columns={
            "score": "grade",
        }
    )
