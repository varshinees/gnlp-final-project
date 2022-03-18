import json
import random
 
# Opening JSON file
f = open('vqacp_v2_test_questions.json')
questions = json.load(f)

person_words = ["person", "man ", "woman", "men ", "women", "children", "child"]
img_ids = []

i = random.randint(0, len(questions) - 1)
# pick out 150 images, with extras if we can't replace them manually
while len(img_ids) < 150:
    if (any(word in questions[i]["question"] for word in person_words) 
            and questions[i]["image_id"] not in img_ids):
        img_ids.append(questions[i]["image_id"])
        print(questions[i]["question"], questions[i]["image_id"])

    i = random.randint(0, len(questions) - 1)

print(img_ids)