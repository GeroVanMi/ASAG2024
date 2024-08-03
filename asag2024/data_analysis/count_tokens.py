import tiktoken

from pipeline.combine import load_combined_asag2024


def encode_row_prompt(entry, encoding: tiktoken.Encoding):
    prompt = f"""
            Evaluate the student answer below to its reference and grade it with a score of 0, 1, 2, 3, 4 or 5.

            Question: {entry["question"]}
            Correct Reference Answer: {entry["reference_answer"]}
            
            Student Answer: {entry["provided_answer"]}

            Expected output format: 
            Feedback: [YOUR FEEDBACK]
            Grade: [YOUR GRADE]
            """

    return encoding.encode(prompt)


def count_tokens(data_frame):
    enc = tiktoken.encoding_for_model("gpt-4")

    encodings = data_frame.apply(encode_row_prompt, axis=1, encoding=enc)
    number_of_tokens = encodings.map(len)
    return sum(number_of_tokens)


if __name__ == "__main__":
    df = load_combined_asag2024()
    number_of_tokens = count_tokens(df)
    print(f"There are {number_of_tokens:,} tokens in the dataset.")
