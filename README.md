# gnlp-final-project
A repo for our Spring 2022 GNLP final project, where we test common VQA models for racial/gender bias.
---
### Prereqs:
You will need the following files into folder `./annotations` downloaded to run these scripts:
1. VQA Questions: https://computing.ece.vt.edu/~aish/vqacp/vqacp_v2_test_questions.json
2. VQA Annotations: https://computing.ece.vt.edu/~aish/vqacp/vqacp_v2_test_annotations.json
3. COCO Annotations: http://images.cocodataset.org/annotations/annotations_trainval2014.zip (unzip into folder `./annotations/coco`)

---
### How to activate the virtual environment
#### MacOS and Linux
The following commands only need to be run once to set up your virtual environment.
1. `python3 -m pip install --user virtualenv`
2. `python3 -m venv venv`

The following step should be run everytime you need to activate your virtual environment.

3. `source venv/bin/activate`
5. (only run first time) `pip3 install -r requirements.txt`

To exit the virtual environment type `deactivate`

---
#### Windows
The following commands only need to be run once to set up your virtual environment.
1. `py -m pip install --user virtualenv`
2. `py -m venv venv`

The following step should be run everytime you need to activate your virtual environment.

3. `.\venv\Scripts\activate`
5. (only run first time) `pip install -r requirements.txt`

To exit the virtual environment type `deactivate`


