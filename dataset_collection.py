import json
import random
from pycocotools.coco import COCO
import requests


'''
Gets the image IDs for images with people in them and writes them to a text file
'''
def generate_image_ids(questions):
    person_words = ["person", "people", "man ", "woman", "men ", "women", "children", "child"]
    img_ids = []
    splits = []

    i = random.randint(0, len(questions) - 1)
    # pick out 150 images, with extras if we can't replace them manually
    while len(img_ids) < 5:
        if (any(word in questions[i]["question"] for word in person_words) 
                and questions[i]["image_id"] not in img_ids):
            img_ids.append(questions[i]["image_id"])
            splits.append(questions[i]['coco_split'])
            print(questions[i]["question"], questions[i]["image_id"])

        i = random.randint(0, len(questions) - 1)

    with open('image_ids.txt', 'w') as img_file:
        for img in img_ids:
            img_file.write(str(img) + " ")
        img_file.write("\n")

        for split in splits:
            img_file.write(split + " ")

'''
Retrieves the image ids from a text file
'''
def retrieve_img_ids():
    with open("image_ids.txt", 'r') as img_file:
        img_ids = img_file.readline()
        splits = img_file.readline()
    
    img_list = list(map(int, img_ids.split()))
    split_list = splits.split()
    
    return img_list, split_list
        

'''
Gets all the questions for each of these images and writes to a json file.
Does not sort since we only need to do this once
'''
def retrieve_questions(img_ids, questions):
    selected_questions = []
    for i in range(len(questions)):
        if any(img == questions[i]['image_id'] for img in img_ids):
            # we've picked this question, store it
            selected_questions.append(questions[i])

    # write to json file
    with open("test_questions.json", "w") as f:
        json.dump(selected_questions, f)

    return selected_questions


'''
Gets all the corresponding annotations for each of these questions and writes to a json file
'''
def retrieve_annotations(selected_questions):
    f = open('./annotations/vqacp_v2_test_annotations.json')
    annotations = json.load(f)

    selected_annotations = []
    for i in range(len(annotations)):
        if any(selected_questions[j]['question_id'] == annotations[i]['question_id'] 
                for j in range(len(selected_questions))):
            # we've picked this question, store it
            selected_annotations.append(annotations[i])

    # write to json file
    with open("test_annotations.json", "w") as f:
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
 
    
if __name__ == "__main__":
    # Opening JSON file
    f = open('./annotations/vqacp_v2_test_questions.json')
    questions = json.load(f)

    generate_image_ids(questions) # comment this out if text file already created
    img_ids, img_splits = retrieve_img_ids()
    print("IDS", img_ids)
    print("SPLITS", img_splits)

    selected_qs = retrieve_questions(img_ids, questions)
    retrieve_annotations(selected_qs)

    # download_images(img_ids, img_splits)
    


    