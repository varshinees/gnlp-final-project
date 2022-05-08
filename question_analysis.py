from __future__ import annotations
from cmath import exp
import json
import matplotlib.pyplot as plt
import numpy as np
from scipy.stats import chi2_contingency
from scipy.stats import mannwhitneyu

'''
Generates the breakdown for number of questions per question type
colors = a dictionary with the output of a previous call to generate_question_counts()
'''
def generate_question_counts(annotations, colors=None):
    question_types = {}
    COLORS = ['#e6194B', '#3cb44b', '#ffe119', '#4363d8', '#f58231', '#911eb4', '#42d4f4', '#f032e6', 
              '#bfef45', '#fabed4', '#469990', '#dcbeff', '#9A6324', '#fffac8', '#800000', '#aaffc3', 
              '#808000', '#ffd8b1', '#000075', '#a9a9a9', '#ffffff', '#000000']
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

'''
datasets: {question_type: {count, percentage}}
''' 
def create_histogram(dataset1: dict[str, int], dataset2: dict[str, int], label1: str, label2: str, color1: str, color2: str):
    NUM_TO_KEEP = 15
    # sum1 = sum(c[0] for _,c in dataset1.items())
    # sum2 = sum(c[0] for _,c in dataset2.items())
    sum1 = 1
    sum2 = 1

    sorted_types = [{"type": q, "count": c[0] / sum1, "accuracy": c[1]} for q,c in dataset1.items()]
    # sorts the questions
    sorted_types.sort(key=lambda x: x["count"], reverse=True)
    
    sorted_types2 = []
    for t in sorted_types:
        if t['type'] in dataset2:
            # the question is in both datasets
            sorted_types2.append({"type": t['type'], "count": dataset2[t['type']][0] / sum2, 
                                    "accuracy": dataset2[t['type']][1]})
    #     else:
    #         # the question is in the first dataset but not the second
    #         sorted_types2.append({"type": t['type'], "count": 0, "accuracy": 0}) 

    # # add the questions in the second dataset but not the first
    # new_questions = list(filter(lambda x: x[0] not in (t['type'] for t in sorted_types), dataset2.items()))
    # sorted_types2.extend({"type": q, "count": c[0] / sum2, "accuracy": c[1]} for q,c in new_questions)
    # sorted_types.extend({"type": q, "count": 0, "accuracy": 0} for q,_ in new_questions)

    w = 0.3
    x = np.arange(15)
    bar_plot = plt.subplot(111)
    b1 = bar_plot.bar(x, tick_label=[t["type"] for t in sorted_types[:NUM_TO_KEEP]], 
                 height = [t["accuracy"] for t in sorted_types[:NUM_TO_KEEP]], color=color1, align='center', width=w)
    b2 = bar_plot.bar(x+w, tick_label=[t["type"] for t in sorted_types2[:NUM_TO_KEEP]], 
                 height = [t["accuracy"] for t in sorted_types2[:NUM_TO_KEEP]], color=color2, align='center', width=w)
    
    plt.xticks(rotation=20, ha='right')
    bar_plot.set_title("GVQA Accuracies by Question Type")
    bar_plot.legend((b1, b2), (label1, label2), loc='upper right')
    bar_plot.set_ylabel('percentage of all question types')
    # plt.show()

    return sorted_types, sorted_types2, sum1, sum2

'''
Conducts the chi-squared test on the two distributions
Parameters are arrays that are outputted from create_histogram()

'''
def calculate_chisquare(expected, observed, exp_sum, obs_sum):
    np.seterr(divide='ignore', invalid='ignore')
    obs = list(map(lambda x: x * obs_sum, [item['count'] for item in observed]))
    exp = list(map(lambda x: x * exp_sum, [item['count'] for item in expected]))
    
    print("Sizes: ", len(obs), len(exp))
    stat, p, dof, expected_vals = chi2_contingency([obs, exp])
    print("Chi2:", stat, p)

    u_res = mannwhitneyu(obs, exp)
    print("U Test:", u_res.statistic, u_res.pvalue)

    
if __name__ == "__main__":
    # # Opening JSON file
    f = open('./annotations/vqacp_v2_test_annotations.json')
    all_annotations = json.load(f)
    total_types = generate_question_counts(all_annotations)

    people_annotations = json.load(open('./annotations/subset_annotations/people_annotations.json'))
    people_types = generate_question_counts(people_annotations, total_types)

    white_annotations = json.load(open('./annotations/subset_annotations/white_annotations.json'))
    white_types = generate_question_counts(white_annotations, total_types)
    
    # nonwhite_annotations = json.load(open('./annotations/subset_annotations/nonwhite_annotations.json'))
    # nonwhite_types = generate_question_counts(nonwhite_annotations, white_types)

    # mixed_annotations = json.load(open('./mixed_annotations.json'))
    # mixed_types = generate_question_counts(mixed_annotations, white_types)
    print(len(people_annotations), len(people_annotations) / len(all_annotations))
    # create_pie_chart(people_types)
    expected, observed, exp_sum, obs_sum = create_histogram(people_types, white_types)
    calculate_chisquare(expected, observed, exp_sum, obs_sum)
    # print(generate_balanced_subset())



