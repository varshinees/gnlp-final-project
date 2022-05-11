import json
from bisect import bisect_left
from math import sqrt
import numpy as np
from question_analysis import create_histogram_result, generate_question_counts
from scipy.stats import chi2_contingency, mannwhitneyu

GVQA_RESULTS_FILE = "gvqa_results.json"
RUBI_RESULTS_FILE = "./results/rubi/rubi_results.json"
BASELINE_VQACP = "./results/baseline_vqacp2/baseline_vqacp2_results.json"

# helper function to do binary search
def binary_search(arr, tgt):
    i = bisect_left(arr, tgt)
    if i != len(arr) and arr[i] == tgt:
        return i
    return -1

# extracts the results for just the results that are in the subset
def extract_results(annotations_file, results, output_filename):
    annotations = json.load(open(annotations_file))
    question_ids = [q['question_id'] for q in annotations]
    question_ids.sort()

    subset_results = []
    for result in results:
        if binary_search(question_ids, result['question_id']) != -1:
            subset_results.append(result)

    json.dump(subset_results, open(output_filename, "w"))


def do_statistical_test(accuracy1, accuracy2, n1, n2):
    total_p = ((accuracy1 * n1) + (accuracy2 * n2)) / (n1 + n2)
    z = (accuracy1 - accuracy2) / sqrt(total_p * (1-total_p) * ((1/n1) + (1/n2)))
    significant = z <= -1.960 or z >= 1.960
    print(z, significant)

'''
input = {question_type: (count, percent_accuracy)}
'''
def calculate_weighted_accuracy(overall_accuracy, subset_accuracy):
    sum_overall = sum(counts[0] for _, counts, in overall_accuracy.items())

    weighted_accuracy = 0
    for question, (_, accuracy) in subset_accuracy.items():
        if question in overall_accuracy:
            weighted_accuracy += accuracy * (overall_accuracy[question][0] / sum_overall)

    return weighted_accuracy



if __name__ == "__main__":
    total_types = json.load(open('./accuracies/gvqa/gvqa_accuracy.json'))

    # people_types = json.load(open('./accuracies/gvqa_accuracy.json'))

    '''
    white_counts: {question_type: (count, color)}
    white_types: {question_type: percent_accuracy}
    output: {question_type: (count, percent_accuracy)}
    '''

    '''
        White: 549
        Nonwhite: 127
        People: 73771
        Overall: 219928
        Mixed: 295
    '''
    do_statistical_test(.4011, .4965, 219928, 127)

    # white_types = json.load(open('./accuracies/gvqa/white_accuracy.json'))
    # white_annotations = json.load(open('./annotations/subset_annotations/white_annotations.json'))
    # white_counts = generate_question_counts(white_annotations)

    # white_output = {key: (white_counts[key][0], white_types[key]) 
    #                 for key in set(white_types.keys()) & set(white_counts.keys())}

    # nonwhite_types = json.load(open('./accuracies/gvqa/nonwhite_accuracy.json'))
    # nonwhite_annotations = json.load(open('./annotations/subset_annotations/nonwhite_annotations.json'))
    # nonwhite_counts = generate_question_counts(nonwhite_annotations)

    # nonwhite_output = {key: (nonwhite_counts[key][0], nonwhite_types[key]) 
    #                 for key in set(nonwhite_types.keys()) & set(nonwhite_counts.keys())}


    # mixed_types = json.load(open('./accuracies/gvqa/mixed_accuracy.json'))
    # mixed_annotations = json.load(open('./annotations/subset_annotations/mixed_annotations.json'))
    # mixed_counts = generate_question_counts(mixed_annotations)

    # mixed_output = {key: (mixed_counts[key][0], mixed_types[key]) 
    #                 for key in set(mixed_types.keys()) & set(mixed_counts.keys())}

    # people_types = json.load(open('./accuracies/gvqa/people_accuracy.json'))
    # people_annotations = json.load(open('./annotations/subset_annotations/people_annotations.json'))
    # print(len(people_annotations))
    # people_counts = generate_question_counts(people_annotations)

    # people_output = {key: (people_counts[key][0], people_types[key]) 
    #                 for key in set(people_types.keys()) & set(people_counts.keys())}

    # print(calculate_weighted_accuracy(people_output, white_output))


    # overall_types = json.load(open('./accuracies/gvqa/gvqa_accuracy.json'))
    overall_annotations = json.load(open('./annotations/vqacp_v2_test_annotations.json'))
    # overall_counts = generate_question_counts(overall_annotations)
    print(len(overall_annotations))

    # overall_output = {key: (overall_counts[key][0], overall_types[key]) 
    #                 for key in set(overall_types.keys()) & set(overall_counts.keys())}

    # # mixed_types = json.load(open('./accuracies/mixed_accuracy.json'))

    # expected, observed, sum1, sum2 = create_histogram_result(white_output, nonwhite_output, 
    #                                             "accuracies for white images", 
    #                                             "accuracies for mixed images", 
    #                                             "blue", "black")
    
    # calculate_chisquare(expected, observed, sum1, sum2)

    # results = json.load(open(BASELINE_VQACP))
    # extract_results("./annotations/subset_annotations/people_annotations.json", 
    #                 results, "./results/baseline_vqacp2/people_results.json")
    # extract_results("./annotations/subset_annotations/mixed_annotations.json", 
    #                 results, "./results/baseline_vqacp2/mixed_race_results.json")
    # extract_results("./annotations/subset_annotations/nonwhite_annotations.json", 
    #                 results, "./results/baseline_vqacp2/nonwhite_results.json")
    # extract_results("./annotations/subset_annotations/white_annotations.json", 
    #                 results, "./results/baseline_vqacp2/white_results.json")              
