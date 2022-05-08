import json
from bisect import bisect_left
import numpy as np
from question_analysis import create_histogram, generate_question_counts
from scipy.stats import chi2_contingency, mannwhitneyu

GVQA_RESULTS_FILE = "gvqa_results.json"
RUBI_RESULTS_FILE = "./results/rubi/rubi_results.json"

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


def calculate_chisquare(expected, observed):
    np.seterr(divide='ignore', invalid='ignore')
    # obs = list(map(lambda x: x * obs_sum, [item['count'] for item in observed]))
    # exp = list(map(lambda x: x * exp_sum, [item['count'] for item in expected]))
    obs = [item['accuracy'] / 100 * item['count'] if item['accuracy'] > 0 else 0 for item in observed ]
    exp = [item['accuracy'] / 100 * item['count'] if item['accuracy'] > 0 else 0 for item in expected]
    
    print("Sizes: ", len(obs), len(exp))
    print(obs)
    print(exp)
    stat, p, dof, expected_vals = chi2_contingency([obs, exp])
    print("Chi2:", stat, p)

    u_res = mannwhitneyu(obs, exp)
    print("U Test:", u_res.statistic, u_res.pvalue)


if __name__ == "__main__":
    total_types = json.load(open('./accuracies/gvqa/gvqa_accuracy.json'))

    # people_types = json.load(open('./accuracies/gvqa_accuracy.json'))

    '''
    white_counts: {question_type: (count, color)}
    white_types: {question_type: percent_accuracy}
    output: {question_type: {count, percentage}}
    '''

    white_types = json.load(open('./accuracies/gvqa/white_accuracy.json'))
    white_annotations = json.load(open('./annotations/subset_annotations/white_annotations.json'))
    white_counts = generate_question_counts(white_annotations)

    white_output = {key: (white_counts[key][0], white_types[key]) 
                    for key in set(white_types.keys()) & set(white_counts.keys())}

    nonwhite_types = json.load(open('./accuracies/gvqa/nonwhite_accuracy.json'))
    nonwhite_annotations = json.load(open('./annotations/subset_annotations/nonwhite_annotations.json'))
    nonwhite_counts = generate_question_counts(nonwhite_annotations)

    nonwhite_output = {key: (nonwhite_counts[key][0], nonwhite_types[key]) 
                    for key in set(nonwhite_types.keys()) & set(nonwhite_counts.keys())}

    # mixed_types = json.load(open('./accuracies/mixed_accuracy.json'))

    expected, observed, _, _ = create_histogram(white_output, nonwhite_output, 
                                                "accuracies for white images", 
                                                "accuracies for nonwhite images", 
                                                "blue", "green")
    
    calculate_chisquare(expected, observed)

    # results = json.load(open(RUBI_RESULTS_FILE))
    # extract_results("./annotations/subset_annotations/people_annotations.json", 
    #                 results, "./results/rubi/people_results.json")
    # extract_results("./annotations/subset_annotations/mixed_annotations.json", 
    #                 results, "./results/rubi/mixed_race_results.json")
    # extract_results("./annotations/subset_annotations/nonwhite_annotations.json", 
    #                 results, "./results/rubi/nonwhite_results.json")
    # extract_results("./annotations/subset_annotations/white_annotations.json", 
    #                 results, "./results/rubi/white_results.json")              
