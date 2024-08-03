import re
from pathlib import Path

import pandas as pd


def extract_grade(llm_answer: str):
    """
    Extracts the first digit after the word "grade".
    """
    trimmed_llm_answer = llm_answer.replace("\n", "")
    grade_match = re.search(r"(G|grade)((?![0-5]).*)([0-5])", trimmed_llm_answer)
    if grade_match is not None:
        return grade_match.group(3)

    raise ValueError(f"Failed to match the grade in:\n{llm_answer}")


def extract_grade_from_file(path: Path):
    with open(path, mode="r") as file:
        llm_answer = file.read()
        return extract_grade(llm_answer)


if __name__ == "__main__":
    # This script updates the values that couldn't be parsed during inference
    project_dir = Path(__file__).resolve().parents[1]

    predictions_path = project_dir.joinpath("data/processed/llama3_predictions.pq")
    df = pd.read_parquet(predictions_path).copy()

    missing_values_dir = project_dir.joinpath("data/processed/llm_errors")
    error_files = missing_values_dir.glob("*.txt")

    for file in error_files:
        try:
            grade = extract_grade_from_file(file)
        except ValueError as error:
            print(error)
            grade = "0"

        df.loc[int(file.stem), "predicted_grade"] = grade

    df.to_parquet(predictions_path)
    print("Sucessfully updated missing values.")
