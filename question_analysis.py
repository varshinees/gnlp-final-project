from __future__ import annotations
import json
import matplotlib.pyplot as plt

'''
Generates the breakdown for number of questions per question type
colors = a dictionary with the output of a previous call to generate_question_counts()
'''
def generate_question_counts(annotations, colors=None):
    question_types = {}
    COLORS = ['#e6194B', '#3cb44b', '#ffe119', '#4363d8', '#f58231', '#911eb4', '#42d4f4', '#f032e6', '#bfef45', '#fabed4', '#469990', '#dcbeff', '#9A6324', '#fffac8', '#800000', '#aaffc3', '#808000', '#ffd8b1', '#000075', '#a9a9a9', '#ffffff', '#000000']
    color_index = 0
    for annotation in annotations:
        if annotation['question_type'] in question_types:
            count = question_types[annotation['question_type']][0]
            color = question_types[annotation['question_type']][1]
            question_types[annotation['question_type']] = (count + 1, color)
        elif colors is None or annotation['question_type'] not in colors:
            # assign a random color
            rand_color = COLORS[color_index]
            question_types[annotation['question_type']] = (1, rand_color)
            color_index = (color_index + 1) % len(COLORS)
        else:
            # get color from colors dict
            question_types[annotation['question_type']] = (1, colors[annotation['question_type']][1])

    return question_types

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

'''
Creates a pie chart showing the question type breakdown
'''
def create_pie_chart(question_types: dict[str, int]):
    NUM_TO_KEEP = 15
    sorted_types = [{"type": q, "count": c[0], "color": c[1]} for q,c in question_types.items()]
    sorted_types.sort(key=lambda x: x["count"], reverse=True)
    other_count = sum(x["count"] for x in sorted_types[NUM_TO_KEEP:])
    sorted_types = sorted_types[0:NUM_TO_KEEP]
    sorted_types.append({"type": "other", "count": other_count, "color": '#03cffc'})
    
    _, _, autopcts = plt.pie([float(v['count']) for v in sorted_types], labels=[str(k['type']) for k in sorted_types], 
            autopct = '%.0f%%', colors=[str(k['color']) for k in sorted_types])
    plt.setp(autopcts, **{'fontsize':8})
    plt.axis('equal')
    plt.show()
    
def create_histogram(dataset1: dict[str, int], dataset2: dict[str, int]):
    n_bins = 10
    NUM_TO_KEEP = 15
    sorted_types = [{"type": q, "count": c[0], "color": c[1]} for q,c in dataset1.items()]
    sorted_types.sort(key=lambda x: x["count"], reverse=True)
    other_count = sum(x["count"] for x in sorted_types[NUM_TO_KEEP:])
    sorted_types = sorted_types[0:NUM_TO_KEEP]
    
    sorted_types2 = [{"type": q, "count": c[0], "color": c[1]} for q,c in dataset2.items()]
    sorted_types2.sort(key=lambda x: x["count"], reverse=True)
    other_count2 = sum(x["count"] for x in sorted_types2[NUM_TO_KEEP:])
    sorted_types2 = sorted_types2[0:NUM_TO_KEEP]

    questions_1 = [str(k['type']) for k in sorted_types]
    questions_2 = [str(k['type']) for k in sorted_types2]
    
    plt.hist([questions_1, questions_2], n_bins)
    plt.show()
    
if __name__ == "__main__":
    # # Opening JSON file
    f = open('./annotations/vqacp_v2_test_annotations.json')
    all_annotations = json.load(f)
    total_types = generate_question_counts(all_annotations)

    # people_annotations = json.load('./all_people_annotations.json')
    # people_types = generate_question_counts(people_annotations, all_annotations)

    white_annotations = json.load(open('./white_annotations.json'))
    white_types = generate_question_counts(white_annotations, all_annotations)
    
    nonwhite_annotations = json.load(open('./nonwhite_annotations.json'))
    nonwhite_types = generate_question_counts(nonwhite_annotations, white_types)
    

    create_pie_chart(total_types)
    # create_histogram(white_types, nonwhite_types)
    # print(generate_balanced_subset())



