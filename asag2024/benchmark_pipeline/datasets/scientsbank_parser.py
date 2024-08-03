import xml.etree.ElementTree as ET
from pathlib import Path

import pandas as pd

from asag2024.benchmark_pipeline.datasets.accuracy_conversion import \
    convert_accuracy_to_grade
from asag2024.configuration import SCIENTSBANK_DATASET_PATH


def parse_file(file: Path):
    """
    Returns a list of entries in the file containing
    question, student_answer, accuracy and file_name.
    """
    parsed_xml = ET.parse(file)
    root = parsed_xml.getroot()

    question = root.find("questionText").text  # type: ignore
    reference_answer = root.find("referenceAnswers").find("referenceAnswer").text  # type: ignore

    student_answer_elements = root.find("studentAnswers").findall(
        "studentAnswer"
    )  # type:ignore

    entries = []
    for student_answer in student_answer_elements:
        entries.append(
            {
                "question": question,
                "student_answer": student_answer.text,
                "accuracy": student_answer.attrib["accuracy"],
                "file_name": file.stem,
                "reference_answer": reference_answer,
            }
        )
    return entries


def rename_scientsbank(sciEntsBank_df) -> pd.DataFrame:
    return sciEntsBank_df.rename(columns={"student_answer": "provided_answer"})


def load_scientsbank(path: Path = SCIENTSBANK_DATASET_PATH):
    splits = [
        "train",
        "test-unseen-answers",
        "test-unseen-questions",
        "test-unseen-domains",
    ]

    split_dataframes = []
    for split in splits:
        split_path = path.joinpath(f"{split}/Core")
        xml_files = list(split_path.glob("*.xml"))
        entries = []

        assert (
            len(xml_files) > 0
        ), "Could not parse SciEntsBank files. Maybe the data is missing?"

        for file in xml_files:
            entries += parse_file(file)

        df = pd.DataFrame(entries)
        df["grade"] = df["accuracy"].apply(convert_accuracy_to_grade)
        df["split"] = split
        split_dataframes.append(df)

    return pd.concat(split_dataframes)


if __name__ == "__main__":
    df = load_scientsbank()
    print(df.head())
