def convert_accuracy_to_grade(accuracy: str):
    if accuracy == "non_domain" or accuracy == "irrelevant":
        return 0
    if accuracy == "contradictory":
        return 1
    if accuracy == "partially_correct_incomplete":
        return 2
    if accuracy == "correct":
        return 3

    raise RuntimeError(f"Unexpected accuracy type encountered: {accuracy}")
