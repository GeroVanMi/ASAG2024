import pandas as pd
from sklearn.preprocessing import MinMaxScaler

from asag2024.benchmark_pipeline.datasets.beetle_parser import (load_beetle,
                                                                rename_beetle)
from asag2024.benchmark_pipeline.datasets.cunlp_loader import (load_cunlp,
                                                               rename_cunlp)
from asag2024.benchmark_pipeline.datasets.digiklausur_loader import (
    convert_grade_to_numeric, load_digiklausur, rename_digiklausur,
    select_necessary_from_digiklausur)
from asag2024.benchmark_pipeline.datasets.mohler_parser import (load_mohler,
                                                                rename_mohler)
from asag2024.benchmark_pipeline.datasets.saf_loader import (load_saf,
                                                             rename_saf)
from asag2024.benchmark_pipeline.datasets.scientsbank_parser import (
    load_scientsbank, rename_scientsbank)
from asag2024.benchmark_pipeline.datasets.stita_loader import (load_stita,
                                                               rename_stita)
from asag2024.benchmark_pipeline.weight_grades import calculate_weights
from asag2024.configuration import COMBINED_DATASET_PATH


def load_combined_asag2024(
    cache_path=COMBINED_DATASET_PATH,
):
    if cache_path.exists():
        return pd.read_parquet(cache_path)

    combined_data = combine_datasets()
    weights = calculate_weights(combined_data)
    # We don't want to use the IDs from the original dataframes because then they won't be unique!
    combined_data.reset_index(inplace=True, drop=False)
    combined_data.to_parquet(cache_path)
    return combined_data


def combine_datasets():
    datasets = load_datasets()
    datasets = list(map(normalize_grade, datasets))

    combined = pd.concat(datasets)
    combined.drop(
        columns=[
            "reference_answer1",
            "reference_answer2",
            "file_name",
            "accuracy",
            "assignment",
            "student_id",
            "id",
            "answer_feedback",
            "verification_feedback",
            "correct",
        ],
        inplace=True,
    )

    return combined


def normalize_grade(dataset) -> pd.DataFrame:
    scaler = MinMaxScaler()
    dataset["normalized_grade"] = scaler.fit_transform(dataset[["grade"]])
    return dataset


def load_datasets():
    beetle = load_beetle()
    beetle = rename_beetle(beetle)
    beetle["data_source"] = "Beetle"

    saf = load_saf()
    saf = rename_saf(saf)
    saf["data_source"] = "SAF"

    mohler = load_mohler()
    mohler = rename_mohler(mohler)
    mohler["data_source"] = "Mohler"

    cunlp = load_cunlp()
    cunlp = rename_cunlp(cunlp)
    cunlp["data_source"] = "CU-NLP"

    stita = load_stita()
    stita = rename_stita(stita)
    stita["data_source"] = "Stita"

    sciEntsBank = load_scientsbank()
    sciEntsBank = rename_scientsbank(sciEntsBank)
    sciEntsBank["data_source"] = "SciEntsBank"

    digiklausur = load_digiklausur()
    digiklausur = rename_digiklausur(digiklausur)
    digiklausur = select_necessary_from_digiklausur(digiklausur)
    digiklausur = convert_grade_to_numeric(digiklausur)
    digiklausur["data_source"] = "DigiKlausur"

    return [beetle, saf, mohler, cunlp, stita, sciEntsBank, digiklausur]


if __name__ == "__main__":
    df = load_combined_asag2024()
