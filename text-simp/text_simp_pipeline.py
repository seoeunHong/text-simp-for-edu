from trained_models import evaluation_functions
import text_simp_math
import text_simp_sci
import openai
import os
import json
import pickle
import spacy
from datasets import load_dataset
import numpy as np
import pandas as pd
import re
import time

openai_model = "gpt-4"

ANS_RE = re.compile(r"#### (\-?[0-9\.\,]+)")
INVALID_ANS = "[invalid]"

def calculate_one_text_score(text,category):
    # The function computes the category score (Lexile\lexical\syntax\decodability) for the given text.
    category = category.lower()
    nlp = spacy.load("en_core_web_sm")
    if category == "lexical":
        model_save_path = "trained_models/final_lexical"
        text_score_dict = evaluation_functions.lexical_linguistic_features(text, nlp)
    elif category == "syntax":
        model_save_path = "trained_models/final_syntax"
        text_score_dict = evaluation_functions.syntax_linguistic_features(text, nlp)
    elif category == "decodability":
        model_save_path = "trained_models/final_decodability"
        text_score_dict = evaluation_functions.decodability_linguistic_features(text, nlp)
    else:
        model_save_path = "trained_models/final_Lexile"
        text_score_dict = evaluation_functions.all_linguistic_features(text, nlp)
    with open(model_save_path, 'rb') as model_file:
        model = pickle.load(model_file)
    x = []
    for key, value in text_score_dict.items():
        x.append(value)
    return np.float64(model.predict([x])[0])


# Make Pipeline Function to do experiments

def text_simp_pipeline(data_type, exp_type, prompt_detail, target_lexile, category):
    print("Start Running...")
    data_type, exp_type, prompt_detail = data_type.lower(), exp_type.lower(), prompt_detail.lower()
    sampels_num = 50
    iterations_num = 3

    if data_type == "math":
        dataset_name = "gsm8k"
        if exp_type == "minimal":
            text_simp_math.minimal_lexile_score(dataset_name, sampels_num, iterations_num, prompt_detail)
        elif exp_type == "target":
            text_simp_math.target_lexile_score(dataset_name, sampels_num, iterations_num, prompt_detail, target_lexile)
        elif exp_type == "one_axis":
            text_simp_math.one_axis_lexile_score(dataset_name, sampels_num, iterations_num, prompt_detail, category)
    elif data_type == "science":
        dataset_name = "/problem_dataset/filtered_science.json"
        if exp_type == "minimal":
            text_simp_sci.minimal_lexile_score(dataset_name, sampels_num, iterations_num, prompt_detail)
        elif exp_type == "target":
            text_simp_sci.target_lexile_score(dataset_name, sampels_num, iterations_num, prompt_detail, target_lexile)
        elif exp_type == "one_axis":
            text_simp_sci.one_axis_lexile_score(dataset_name, sampels_num, iterations_num, prompt_detail, category)
    else:
        print("There is no such dataset")
        return
    
    print("Experiment Is Done See The Result at experiment_results folder")



if __name__ == '__main__':
    DATA_TYPE = "math" #science
    EXP_TYPE = "minimal" #target #one_axis
    PROMPT_DETAIL = "base" #knowledge #formula #fewshots
    TARGET_LEXILE = None #700 #900 #1200
    CATEGORY = None #syntax #lexical #decodability
    text_simp_pipeline(DATA_TYPE, EXP_TYPE, PROMPT_DETAIL, TARGET_LEXILE, CATEGORY)