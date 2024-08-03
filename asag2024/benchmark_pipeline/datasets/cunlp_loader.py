from pathlib import Path

import pandas as pd

from asag2024.configuration import CUNLP_DATASET_PATH


def load_cunlp(data_path: Path = CUNLP_DATASET_PATH):
    """
    Loads the data set from the CSV file.
    """
    return pd.read_csv(data_path, sep=";", encoding="cp857", index_col="no")


def rename_cunlp(cunlp_df):
    """
    Renames the columns, "question1" to "provided_answer" and "question2" to "reference_answer".
    This is described in the data set author's paper: https://ieeexplore.ieee.org/document/9335022
    """
    return cunlp_df.rename(
        columns={
            "question1": "provided_answer",
            "question2": "reference_answer",
        }
    )
