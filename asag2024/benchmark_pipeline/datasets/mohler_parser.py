import re
from pathlib import Path

import pandas as pd
from lxml import etree  # type: ignore

from asag2024.configuration import MOHLER_DATASET_PATH


def remove_html_tags(text):
    parser = etree.HTMLParser()
    tree = etree.fromstring(text, parser)
    return etree.tostring(tree, encoding="utf-8", method="text")


def parse_mohler(
    data_folder_path: Path = MOHLER_DATASET_PATH,
) -> list[dict]:
    entries = []
    for assignment_index in range(1, 4):
        with open(
            data_folder_path.joinpath(f"assign{assignment_index}.txt"),
            mode="r",
            encoding="utf-8",
        ) as file:
            current_question = ""
            current_reference_answer = ""

            for line in file:
                line = line.strip()
                if line == "":
                    continue

                if line.startswith("#"):
                    continue

                if line.startswith("Question"):
                    current_question = line.split(": ")[1]
                    continue

                if line.startswith("Answer"):
                    current_reference_answer = line.split(": ")[1]
                    continue

                grade, student_id, student_answer = re.split(r"	\[|\]	", line)
                entries.append(
                    {
                        "assignment": assignment_index,
                        "question": current_question,
                        "reference_answer": current_reference_answer,
                        "grade": float(grade),
                        "student_id": int(student_id),
                        "student_answer": remove_html_tags(student_answer),
                    }
                )
    return entries


def load_mohler():
    df = pd.DataFrame(parse_mohler())
    df["student_answer"] = df["student_answer"].str.decode("utf-8")
    return df


def rename_mohler(mohler: pd.DataFrame) -> pd.DataFrame:
    return mohler.rename(columns={"student_answer": "provided_answer"})
