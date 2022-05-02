import json
from bisect import bisect_left
import time
from collections import Counter

GVQA_RESULTS_FILE = "gvqa_results.json"

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


if __name__ == "__main__":
    results = json.load(open(GVQA_RESULTS_FILE))
    extract_results("./annotations/subset_annotations/all_people_annotations.json", 
                    results, "./results/all_people_results.json")
    extract_results("./annotations/subset_annotations/mixed_annotations.json", 
                    results, "./results/mixed_race_results.json")
    extract_results("./annotations/subset_annotations/nonwhite_annotations.json", 
                    results, "./results/nonwhite_results.json")
    extract_results("./annotations/subset_annotations/white_annotations.json", 
                    results, "./results/white_results.json")              
