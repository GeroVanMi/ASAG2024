import xml.etree.ElementTree as ET
from pathlib import Path

import pandas as pd

from asag2024.benchmark_pipeline.datasets.accuracy_conversion import \
    convert_accuracy_to_grade
from asag2024.configuration import BEETLE_DATASET_PATH


def parse_file(file: Path):
    """
    Returns a list of entries in the file containing
    question, student_answer, accuracy and file_name.
    """
    parsed_xml = ET.parse(file)
    root = parsed_xml.getroot()

    question = root.find("questionText").text  # type: ignore
    reference_answer_elements = root.find("referenceAnswers").findall("referenceAnswer")  # type: ignore
    reference_answers = []
    for ref_answer in reference_answer_elements:
        if ref_answer.attrib["category"] == "BEST":
            reference_answers.append(ref_answer.text)

    student_answer_elements = root.find("studentAnswers").findall("studentAnswer")  # type: ignore

    entries = []
    for student_answer in student_answer_elements:
        entry = {
            "question": question,
            "student_answer": student_answer.text,
            "accuracy": student_answer.attrib["accuracy"],
            "file_name": file.stem,
        }
        for index, reference_answer in enumerate(reference_answers):
            entry[f"reference_answer{index}"] = reference_answer
        entries.append(entry)
    return entries


def load_beetle(
    xml_folder_path=BEETLE_DATASET_PATH,
) -> pd.DataFrame:
    xml_files = xml_folder_path.glob("*.xml")

    entries = []
    for file in xml_files:
        entries += parse_file(file)

    df = pd.DataFrame(entries)
    df["grade"] = df["accuracy"].apply(convert_accuracy_to_grade)
    return df


def rename_beetle(beetle: pd.DataFrame) -> pd.DataFrame:
    return beetle.rename(
        columns={
            "reference_answer0": "reference_answer",
            "student_answer": "provided_answer",
        }
    )
