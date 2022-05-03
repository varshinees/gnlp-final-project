import json
import random
from bisect import bisect_left, insort
from pycocotools.coco import COCO
import requests
import os

def binary_search(arr, tgt, key=None):
    i = bisect_left(arr, tgt, key=(lambda x: x[key]) if key is not None else None)
    if key is None:
        if i != len(arr) and arr[i] == tgt:
            return i
    else:
        if i != len(arr) and arr[i][key] == tgt:
            return i
    return -1

'''
Gets the image IDs for images with people in them and writes them to a text file
'''
def generate_image_ids(questions):
    person_words = ["person", "people", "man ", "woman", "men ", "women", "children", "child"]
    img_ids = []

    i = random.randint(0, len(questions) - 1)
    # pick out 150 images, with extras if we can't replace them manually
    while len(img_ids) < 1100:
        if (any(word in questions[i]["question"] for word in person_words) 
                and questions[i]["image_id"] not in img_ids):
            img_ids.append({
                'image_id': questions[i]["image_id"], 
                'split': questions[i]['coco_split']
                })

            print(questions[i]["question"], questions[i]["image_id"])

        i = random.randint(0, len(questions) - 1)

    with open('image_ids.json', 'w') as img_file:
        json.dump(img_ids, img_file)

'''
Retrieves the image ids from a text file
'''
def retrieve_img_ids(image_path):
    img_file = open(image_path, 'r')
    images = json.load(img_file)   

    img_list = [img['image_id'] for img in images]   
    split_list = [img['split'] for img in images]  
    
    return img_list, split_list
        

'''
Gets all the questions for each of these images and writes to a json file.
Does not sort since we only need to do this once
'''
def retrieve_questions(img_ids, questions, file_name="test_questions.json"):
    img_ids.sort()
    selected_questions = []
    for q in questions:
        if binary_search(img_ids, q['image_id']) != -1:
            # we've picked this question, store it
            selected_questions.append(q)

    # write to json file
    with open(file_name, "w") as f:
        json.dump(selected_questions, f)

    return selected_questions


'''
Gets all the corresponding annotations for each of these questions and writes to a json file
'''
def retrieve_annotations(selected_questions, file_name="test_annotations.json"):
    f = open('./annotations/vqacp_v2_test_annotations.json')
    annotations = json.load(f)
    annotations.sort(key=lambda x: x["question_id"])

    selected_annotations = []
    for q in selected_questions:
        idx = binary_search(annotations, q["question_id"], key="question_id")
        selected_annotations.append(annotations[idx])

    # write to json file
    with open(file_name, "w") as f:
        json.dump(selected_annotations, f)


'''
Downloads each of the images from the COCO dataset
'''
def download_images(img_ids, img_splits):
    coco_train = COCO('./annotations/coco/instances_train2014.json') 
    coco_val = COCO('./annotations/coco/instances_val2014.json')
    
    train_ids = [img_ids[i] for i in range(len(img_ids)) if img_splits[i] == "train2014"]
    val_ids = [img_ids[i] for i in range(len(img_splits)) if img_splits[i] == "val2014"]
           
    images_train = coco_train.loadImgs(train_ids) 
    images_val = coco_val.loadImgs(val_ids)
    
    # save the images to a local folder
    for im in images_train:
        img_data = requests.get(im['coco_url']).content
        with open('./original_img/' + im['file_name'], 'wb') as handler: 
            handler.write(img_data)
    for im in images_val:
        img_data = requests.get(im['coco_url']).content
        with open('./original_img/' + im['file_name'], 'wb') as handler: 
            handler.write(img_data)
 
'''
Generates the image ids from a given folder
'''
def generate_image_ids_from_folder(folder_path, output_path):
    directory = os.fsencode(folder_path)
    output_dict = []
    for file in os.listdir(directory):
        filename = os.fsdecode(file)
        if filename.endswith(".jpg"): 
            file_parts = filename[:-4].split('_')
            split = file_parts[1]
            id = int(file_parts[2])
            output_dict.append({"image_id": id, "split": split})
        else:
            continue
    
    #write to json file
    with open(output_path, "w") as f:
        json.dump(output_dict, f)


'''
Counts proportion of people-based questions in the full dataset
'''
def select_people_imgs(questions):
    person_words = ["person", "people", "man ", "woman", "men ", "women", "children", "child"]
    img_ids = []

    # picks image ids
    for q in questions:
        if (any(word in q["question"] for word in person_words) 
                and binary_search(img_ids, q["image_id"]) == -1):
            insort(img_ids, q["image_id"])

    with open('./annotations/image_ids/people_image_ids.json', 'w') as img_file:
        json.dump(img_ids, img_file)

    return img_ids


if __name__ == "__main__":
    # # Opening JSON file
    f = open('./annotations/vqacp_v2_test_questions.json')
    questions = json.load(f)

    # generate_image_ids(questions) # comment this out if text file already created
    # generate_image_ids_from_folder("./white_imgs", "white_image.json")
    # img_ids, img_splits = retrieve_img_ids("./annotations/image_ids/white_image_ids.json")
    # download_images(img_ids, img_splits)

    # comment this in once images have been curated
    # selected_qs = retrieve_questions(img_ids, questions, "./annotations/subset_questions/white_questions.json")
    selected_img_ids = select_people_imgs(questions)
    selected_qs = retrieve_questions(selected_img_ids, questions, "./annotations/subset_questions/people_questions.json")
    retrieve_annotations(selected_qs, "./annotations/subset_annotations/people_annotations.json")
    
    # TODO: Change the generate_image_ids method to read test_image_ids.json and generate images not in there to gather more data


    


    