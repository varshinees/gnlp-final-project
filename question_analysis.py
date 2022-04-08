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

'''
Outputs a json with the question ids for the subset, having balanced to match the full dataset
'''
def generate_balanced_subset(total_types, total_sum, subset_types, subset_sum):
    TARGET_SIZE = 0.5
    # how many questions of each type do we want?
    target_counts = {question_type: (question_count / total_sum) * subset_sum * TARGET_SIZE 
                    for question_type, question_count in total_types.items() }

    subset_questions = json.load(open('./test_annotations.json'))
    questions_to_keep = []
    for question in subset_questions:
        if target_counts[question['question_type']] > 0:
            questions_to_keep.append(question['question_id'])
            target_counts[question['question_type']] -= 1
    
     #write to json file, change the "white"
    with open("subset_questions_white", "w") as f:
        json.dump(questions_to_keep, f)


if __name__ == "__main__":
    # # Opening JSON file
    f = open('./annotations/vqacp_v2_test_annotations.json')
    all_annotations = json.load(f)

    f2 = open('./test_annotations.json')
    subset_annotations = json.load(f2)

    total_types, total_sum = generate_question_counts(all_annotations)
    subset_types, subset_sum = generate_question_counts(subset_annotations)

    print(generate_question_counts(all_annotations))



