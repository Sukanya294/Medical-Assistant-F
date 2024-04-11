import nltk
import pandas as pd
from nltk import ne_chunk, word_tokenize, pos_tag
from nltk.chunk import conlltags2tree, tree2conlltags
import os
import re
import configparser

config = configparser.ConfigParser()
config.read('../config/config.ini')


def download_nltk_resources():
    nltk.download('punkt')
    nltk.download('averaged_perceptron_tagger')
    nltk.download('maxent_ne_chunker')


def generate_absolute_path(relative_path):
    absolute_path = os.path.abspath(relative_path)
    return absolute_path


def get_symptoms_keywords_train_data():
    file_path = generate_absolute_path('../../data/training_data/symptoms.txt')
    with open(file_path, 'r') as f:
        values = f.readlines()
        lines = [line.strip() for line in values]

    return lines


def get_age_pattern_train_data():
    file_path = generate_absolute_path('../../data/training_data/age_pattern.txt')
    with open(file_path, 'r') as f:
        values = f.readlines()
        lines = [line.strip() for line in values]

    return lines


def get_weight_pattern_train_data():
    file_path = generate_absolute_path('../../data/training_data/weight_pattern.txt')
    with open(file_path, 'r') as f:
        values = f.readlines()
        lines = [line.strip() for line in values]

    return lines


def get_name_pattern_train_data():
    file_path = generate_absolute_path('../../data/training_data/name_pattern.txt')
    with open(file_path, 'r') as f:
        values = f.readlines()
        lines = [line.strip() for line in values]

    return lines


def extract_entities(text):
    entities = {
        'name': None,
        'age': None,
        'weight': None,
        'symptoms': None
    }

    # Extract name using pattern matching
    name_patterns = get_name_pattern_train_data()
    for pattern in name_patterns:
        match = re.search(pattern, text)
        if match:
            entities['name'] = match.group(1)
            break

    # Extract age and weight using pattern matching
    age_patterns = get_age_pattern_train_data()
    for pattern in age_patterns:
        match = re.search(pattern, text)
        if match:
            entities['age'] = match.group(1)
            break

    weight_patterns = get_weight_pattern_train_data()
    for pattern in weight_patterns:
        match = re.search(pattern, text)
        if match:
            entities['weight'] = match.group(1)
            break

    # Extract symptoms using keyword matching
    symptoms_keywords = get_symptoms_keywords_train_data()
    for keyword in symptoms_keywords:
        if keyword in text:
            entities['symptoms'] = keyword
            break

    return entities


def highlight_entities(text, entities):
    highlighted_text = text
    for key, value in entities.items():
        if value:
            highlighted_text = highlighted_text.replace(value, f'*{value}*')
    return highlighted_text


def highlight_text(input_file):
    entities_list = []

    with open(input_file, 'r') as file:
        text = file.read()

    entities = extract_entities(text)
    highlighted_text = highlight_entities(text, entities)
    entities_list.append(entities)
    print(entities)

    excel_file_path = generate_absolute_path(f'../../data/excel_report/entities_data.xlsx')
    df = pd.read_excel(excel_file_path)
    df = df._append(entities, ignore_index=True)
    df.to_excel(excel_file_path, index=False)
    print(f'Added below records to excel report {entities}')

    return highlighted_text
