from __future__ import annotations
import json

def generate_question_counts(annotations):
    sum = 0
    question_types = {}
    for annotation in annotations:
        if annotation['question_type'] in question_types:
            question_types[annotation['question_type']] += 1
        else:
            question_types[annotation['question_type']] = 1
        sum += 1

    return question_types, sum


if __name__ == "__main__":
    # # Opening JSON file
    f = open('./annotations/vqacp_v2_test_annotations.json')
    annotations = json.load(f)

    print(generate_question_counts(annotations))



