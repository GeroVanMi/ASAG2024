from pathlib import Path

import pandas as pd
from asag2024.configuration import DIGIKLAUSUR_DATASET_PATH


def load_digiklausur(path: Path = DIGIKLAUSUR_DATASET_PATH):
    return pd.read_csv(path)


def select_necessary_from_digiklausur(df: pd.DataFrame) -> pd.DataFrame:
    return df[["id", "provided_answer", "reference_answer", "grade", "question_id"]]  # type: ignore


def rename_digiklausur(df: pd.DataFrame):
    return df.rename(
        columns={
            "student_answer": "provided_answer",
            "ref_answer": "reference_answer",
            "grades_round": "grade",
            "Unnamed: 0": "id",
        }
    )


def convert_grade_to_numeric(df: pd.DataFrame):
    df["grade"] = df["grade"].astype(int)
    return df
