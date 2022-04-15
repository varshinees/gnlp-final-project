import json
import random
from pycocotools.coco import COCO
import requests
import os


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
    selected_questions = []
    for i in range(len(questions)):
        if any(img == questions[i]['image_id'] for img in img_ids):
            # we've picked this question, store it
            selected_questions.append(questions[i])

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

    selected_annotations = []
    for i in range(len(annotations)):
        if any(selected_questions[j]['question_id'] == annotations[i]['question_id'] 
                for j in range(len(selected_questions))):
            # we've picked this question, store it
            selected_annotations.append(annotations[i])

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
def select_people_questions(questions):
    person_words = ["person", "people", "man ", "woman", "men ", "women", "children", "child"]
    selected_qs = []

    # pick out 150 images, with extras if we can't replace them manually
    for q in questions:
        if (any(word in q["question"] for word in person_words) 
                and q["image_id"] not in selected_qs):
            selected_qs.append(q)

    print(len(selected_qs) / len(questions))
    return selected_qs


if __name__ == "__main__":
    # # Opening JSON file
    f = open('./annotations/vqacp_v2_test_questions.json')
    questions = json.load(f)

    # generate_image_ids(questions) # comment this out if text file already created
    # generate_image_ids_from_folder("./other_races_imgs", "nonwhite_image_ids.json")
    # img_ids, img_splits = retrieve_img_ids("nonwhite_image_ids.json")
    # download_images(img_ids, img_splits)

    # comment this in once images have been curated
    # selected_qs = retrieve_questions(img_ids, questions, "nonwhite_questions.json")
    selected_qs = select_people_questions(questions)
    retrieve_annotations(selected_qs, "all_people_annotations.json")
    
    # TODO: Change the generate_image_ids method to read test_image_ids.json and generate images not in there to gather more data


    


    