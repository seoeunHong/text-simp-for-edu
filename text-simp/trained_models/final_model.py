from trained_models import evaluation_functions
import numpy as np
import pickle
import spacy

def calculate_text_score(text, category):
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