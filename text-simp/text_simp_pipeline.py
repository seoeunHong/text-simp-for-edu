from trained_models import evaluation_functions
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
