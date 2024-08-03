import pandas as pd

# from asag2024_dataset.combine_pipeline import load_combined_asag2024


def calculate_weights(df: pd.DataFrame):
    """
    TODO: Document this or you will regret it!
    Also still contains code duplication that could probably be fixed!
    """
    for data_source in df["data_source"].unique():
        number_of_blocks = 10
        number_of_non_empty_blocks = 0

        for index in range(0, number_of_blocks):
            lower_bound = index / 10
            upper_bound = round(lower_bound + 0.1, 1)

            if index != number_of_blocks - 1:
                condition = (
                    (df["data_source"] == data_source)
                    & (df["normalized_grade"] >= lower_bound)
                    & (df["normalized_grade"] < upper_bound)
                )

            else:
                condition = (
                    (df["data_source"] == data_source)
                    & (df["normalized_grade"] >= lower_bound)
                    & (df["normalized_grade"] <= upper_bound)
                )

            grades = df.loc[condition]
            number_of_entries = len(grades)

            if number_of_entries > 0:
                number_of_non_empty_blocks += 1
            # )

        for index in range(0, number_of_blocks):
            lower_bound = index / 10
            upper_bound = round(lower_bound + 0.1, 1)
            if index != number_of_blocks - 1:
                condition = (
                    (df["data_source"] == data_source)
                    & (df["normalized_grade"] >= lower_bound)
                    & (df["normalized_grade"] < upper_bound)
                )

            else:
                condition = (
                    (df["data_source"] == data_source)
                    & (df["normalized_grade"] >= lower_bound)
                    & (df["normalized_grade"] <= upper_bound)
                )

            grades = df.loc[condition]
            number_of_entries = len(grades)

            if number_of_entries > 0:
                assigned_weight_for_block = 1 / number_of_non_empty_blocks
                weight_per_entry = assigned_weight_for_block / number_of_entries
                df.loc[condition, "weight"] = weight_per_entry
                df.loc[condition, "grade_range"] = f"{lower_bound}-{upper_bound}"
    return df
