import shutil
from pathlib import Path

project_path = Path(__file__).parents[1]

# This is the folder where all of our intermediate outputs are stored
processed_data_path = project_path.joinpath("data/processed")
GRADE_RESULTS_PATH = processed_data_path.joinpath("results.pq")
NOMIC_EMBEDDINGS_PATH = processed_data_path.joinpath("nomic_embeddings.pq")
COMBINED_DATASET_PATH = processed_data_path.joinpath("combined_asag2024.pq")
LLM_RESPONSES_PATH = processed_data_path.joinpath("llm_responses/")
PROMETHEUS_PATH = LLM_RESPONSES_PATH.joinpath("prometheus/")
HUGGINGFACE_OUTPUT_PATH=processed_data_path.joinpath("huggingface_data.pq")

# GPT-4o intermediate and final results
GPT4_BATCH_PROMPTS_PATH = processed_data_path.joinpath("asag2024_prompts.jsonl")
GPT4_JSONL_ANSWERS_PATH = processed_data_path.joinpath("gpt4_answers.jsonl")

# GPT-3 intermediate and final results
GPT3_BATCH_PROMPTS_PATH = processed_data_path.joinpath("asag2024_prompts_gpt3.jsonl")
GPT3_JSONL_ANSWERS_PATH = processed_data_path.joinpath("gpt3_answers.jsonl")

# This is the folder where the final ouputs are stored
results_path = project_path.joinpath("data/results")
GPT4_FINAL_RESULTS_PATH = results_path.joinpath("gpt4_results.pq")
GPT3_FINAL_RESULTS_PATH = results_path.joinpath("gpt3_results.pq")
SAF_BART_PREDICTIONS_PATH = results_path.joinpath("saf_bart_results.pq")
NOMIC_RESULTS_PATH = results_path.joinpath("nomic_results.pq")
RESULTS_TABLE_PATH = results_path.joinpath("result_tables/")

FIGURES_PATH = project_path.joinpath("figures/")

# This is the folder that all the compressed data files get extracted to
original_data_path = project_path.joinpath("data/original")
# TODO: The actual extraction script does not use theses pathes yet!
# Dataset pathes
BEETLE_DATASET_PATH = original_data_path.joinpath("semeval-5way/beetle/train/Core")
SCIENTSBANK_DATASET_PATH = original_data_path.joinpath("semeval-5way/sciEntsBank/")
MOHLER_DATASET_PATH = original_data_path.joinpath("ShortAnswerGrading_v1.0")
CUNLP_DATASET_PATH = original_data_path.joinpath("CU-NLP.csv")
STITA_DATASET_PATH = original_data_path.joinpath("stita.csv")
DIGIKLAUSUR_DATASET_PATH = original_data_path.joinpath("DigiKlausur/asag_dataset.csv")

DOTENV_PATH = project_path.joinpath(".env")

GPT_MODEL_4 = "gpt-4o"
GPT_MODEL_3 = "gpt-3.5-turbo"


# Automatically create the results file if it does not exist.
if not GRADE_RESULTS_PATH.exists() and COMBINED_DATASET_PATH.exists():
    shutil.copyfile(COMBINED_DATASET_PATH, GRADE_RESULTS_PATH)

# Plotting configurations
data_source_colors = [
    "#ef476f",
    "#ffd166",
    "#06d6a0",
    "#26547c",
    "#ff7f50",
    "#7a3e48",
    "#8a8aff",
]
boxplot_width = 300
boxplot_height = 200
boxplot_size = 50

PROMPT_TEMPLATE = """
            Evaluate the student answer below to its reference and grade it with a score of 0, 1, 2, 3, 4 or 5.

            Question: {question}
            Correct Reference Answer: {reference_answer}
            
            Student Answer: {provided_answer}    

            Expected output format: 
            Feedback: [YOUR FEEDBACK]
            Grade: [YOUR GRADE]
            """


def altair_theme():
    font = "JetBrainsMono Nerd Font"
    title_font = "Inter"
    font_size = 8
    return {
        "config": {
            "font": font,
            "title": {},
            "axisX": {
                "labelFontSize": font_size,
                "titleFontSize": font_size,
                "titleFont": title_font,
            },
            "axisY": {
                "labelFontSize": font_size,
                "titleFontSize": font_size,
                "titleFont": title_font,
            },
            "text": {"fontSize": font_size},
        }
    }
