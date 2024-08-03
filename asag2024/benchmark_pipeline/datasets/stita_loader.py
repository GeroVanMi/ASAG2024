import pandas as pd

from asag2024.configuration import STITA_DATASET_PATH


def load_stita(path=STITA_DATASET_PATH) -> pd.DataFrame:
    return pd.read_csv(path, delimiter=";")


def rename_stita(df) -> pd.DataFrame:
    return df.rename(
        columns={
            "dataset": "data_source",
            "score": "grade",
            "answer": "provided_answer",
            "real_answer": "reference_answer",
        }
    )
