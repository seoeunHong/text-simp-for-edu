from matplotlib import pyplot as plt
from linguistic_features import data_pre_processing
import evaluation_functions
import numpy as np
import pickle
import spacy
import seaborn as sns

def coefficients(model_path, features):
    # This function prints the coefficients of the linear regression model

    # features = ['parsing_tree_depth','max_nesting_level','avg_puncuations_num','avg_num_of_entity',
    #             'kuperman AoA','avg_num_pos','avg_uniq_GPCs',' avg_DallChall_words ','avg_words_in_text',
    #             'avg_syllables_in_text','avg_difficult_words_acc_syllabels','avg_num_of_characters','trr']

    with open(model_path, 'rb') as model_file:
        model = pickle.load(model_file)
    features_weight = model.coef_
    for name, score in zip(features, features_weight):
        print(f"{name}: {score}")

def cheack_for_cov():
    # This function checks for correlation/covariance between the models/features

    nlp = spacy.load("en_core_web_sm")
    dataset_path = 'datasets/lexile_dataset.xlsx'
    df = data_pre_processing.read_xlsx_to_df(dataset_path)

    all_features = []
    lexical_features = []
    syntax_features = []
    decodability_features = []
    for index, row in df.iterrows():
        text = row['Content']

        all_features_scores = []
        text_score_dict_all = evaluation_functions.avg_all_linguistic_features(text, nlp)
        for key, value in text_score_dict_all.items():
            all_features_scores.append(value)
        all_features.append(all_features_scores)

        lexical_features_scores = []
        text_score_dict_lexical = evaluation_functions.lexical_linguistic_features(text, nlp)
        for key, value in text_score_dict_lexical.items():
            lexical_features_scores.append(value)
        lexical_features.append(lexical_features_scores)

        syntax_features_scores = []
        text_score_dict_syntax = evaluation_functions.syntax_linguistic_features(text, nlp)
        for key, value in text_score_dict_syntax.items():
            syntax_features_scores.append(value)
        syntax_features.append(syntax_features_scores)

        decodability_features_scores = []
        text_score_dict_decodability = evaluation_functions.decodability_linguistic_features(text, nlp)
        for key, value in text_score_dict_decodability.items():
            decodability_features_scores.append(value)
        decodability_features.append(decodability_features_scores)

    with open('trained_models/LR_avg_lexical_linguistic_features', 'rb') as model_file:
        lexical_model = pickle.load(model_file)
    lexical_pred = lexical_model.predict(lexical_features)

    with open('trained_models/LR_avg_syntax_linguistic_features', 'rb') as model_file:
        syntax_model = pickle.load(model_file)
    syntax_pred = syntax_model.predict(syntax_features)

    with open('trained_models/LR_avg_decodability_linguistic_features', 'rb') as model_file:
        decodability_model = pickle.load(model_file)
    decodability_pred = decodability_model.predict(decodability_features)

    print("corrolation of lexical and decodability is: ", np.corrcoef(lexical_pred, decodability_pred))
    print("corrolation of syntax and decodability is: ", np.corrcoef(syntax_pred, decodability_pred))
    print("corrolation of lexical and syntax is: ", np.corrcoef(lexical_pred, syntax_pred))

    covariance_matrix = np.cov([lexical_pred, syntax_pred, decodability_pred], rowvar=False)

    cov_lexical_syntax = covariance_matrix[0, 1]
    cov_lexical_decodability = covariance_matrix[0, 2]
    cov_syntax_decodability = covariance_matrix[1, 2]

    print("Covariance between lexical and syntax is:", cov_lexical_syntax)
    print("Covariance between lexical and decodability is:", cov_lexical_decodability)
    print("Covariance between syntax and decodability is:", cov_syntax_decodability)

    correlation_matrix = np.corrcoef(all_features, rowvar=False)

    # Create a heatmap using seaborn
    plt.figure(figsize=(8, 6))
    sns.heatmap(correlation_matrix, annot=True, cmap='coolwarm', fmt=".2f",
                xticklabels=    ['parsing tree depth','max nesting level','puncuations num','num of entity','kuperman AoA','num of POS','uniq GPCs','DallChall words',
     'words', 'syllables', 'difficult words acc syllabels','num of charachters','ttr'],
                yticklabels=    ['parsing tree depth','max nesting level','puncuations num','num of entity','kuperman AoA','num of POS','uniq GPCs','DallChall words',
     'words', 'syllables', 'difficult words acc syllabels','num of charachters','ttr'])
    plt.title("Correlation Matrix Heatmap")
    plt.show()

    # Create a covariance matrix using numpy's cov function
    covariance_matrix = np.cov(all_features, rowvar=False)

    # Create a heatmap using seaborn
    plt.figure(figsize=(8, 6))
    sns.heatmap(covariance_matrix, annot=True, cmap='coolwarm', fmt=".2f",
                xticklabels=    ['parsing tree depth','max nesting level','puncuations num','num of entity','kuperman AoA','num of POS','uniq GPCs','DallChall words',
     'words', 'syllables', 'difficult words acc syllabels','num of charachters','ttr'],
                yticklabels=    ['parsing tree depth','max nesting level','puncuations num','num of entity','kuperman AoA','num of POS','uniq GPCs','DallChall words',
     'words', 'syllables', 'difficult words acc syllabels','num of charachters','ttr'])
    plt.title("Covariance Matrix Heatmap")
    plt.show()

if __name__ == '__main__':
    model_path = "trained_models/final_Lexile"
    features_all = ['avg words in text','avg num of charachters','avg parsing tree depth','avg max nesting level','avg puncuations num','avg num of entity','avg num of POS', 'avg DallChall words in text', 'avg syllables in text',  'avg difficult words acc syllabels','avg kuperman AoA',  'ttr', 'avg l_s_d', 'avg GPCs per word']
    coefficients(model_path, features_all)