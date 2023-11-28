from collections import Counter
import lftk
from g2p_en import G2p
from nltk.tokenize import sent_tokenize, word_tokenize
import subprocess
import re


def get_depth(node):
    # Base case: if the node has no children, return 0
    if not list(node.children):
        return 0
    # Recursive case: return 1 plus the maximum depth of the node's children
    else:
        return 1 + max(get_depth(child) for child in node.children)

def parsing_tree_depth(text,nlp):
    list_of_depths = []
    sentences = sent_tokenize(text)
    for sentence in sentences:
        doc = nlp(sentence)
        root = doc[:].root
        depth = get_depth(root)
        list_of_depths.append(depth)
    return sum(list_of_depths)/len(list_of_depths)

def max_nesting_level(text, nlp):
    doc = nlp(text)
    max_nesting = 0
    for token in doc:
        nesting_level = len(list(token.subtree))
        max_nesting = max(max_nesting, nesting_level)
    return max_nesting

def puntuations_num (text,nlp):
    list_of_n_punc = []
    sentences = sent_tokenize(text)
    for sentence in sentences:
        doc = nlp(sentence)
        LFTK = lftk.Extractor(docs=doc)
        extracted_features = LFTK.extract(features=["t_punct"])
        list_of_n_punc.append(extracted_features['t_punct'])
    return sum(list_of_n_punc)

def avg_puncuations_num (text,nlp):
    list_of_n_punc = []
    sentences = sent_tokenize(text)
    for sentence in sentences:
        doc = nlp(sentence)
        LFTK = lftk.Extractor(docs=doc)
        extracted_features = LFTK.extract(features=["t_punct"])
        list_of_n_punc.append(extracted_features['t_punct'])
    return sum(list_of_n_punc)/len(list_of_n_punc)


def num_of_entity (text,nlp):
    list_of_n_entity = []
    sentences = sent_tokenize(text)
    for sentence in sentences:
        doc = nlp(sentence)
        LFTK = lftk.Extractor(docs=doc)
        extracted_features = LFTK.extract(features=["t_n_ent"])
        list_of_n_entity.append(extracted_features['t_n_ent'])
    return sum(list_of_n_entity)

def avg_num_of_entity (text,nlp):
    list_of_n_entity = []
    sentences = sent_tokenize(text)
    for sentence in sentences:
        doc = nlp(sentence)
        LFTK = lftk.Extractor(docs=doc)
        extracted_features = LFTK.extract(features=["t_n_ent"])
        list_of_n_entity.append(extracted_features['t_n_ent'])
    return sum(list_of_n_entity)/len(list_of_n_entity)

def kuperman_AoA(text,nlp):
    # It has already been implemented to take the average of all sentences
    doc = nlp(text)
    LFTK = lftk.Extractor(docs=doc)
    extracted_features = LFTK.extract(features=["a_kup_ps"])
    return extracted_features['a_kup_ps']


def brysbaer_AoA(text,nlp):
    doc = nlp(text)
    LFTK = lftk.Extractor(docs=doc)
    extracted_features = LFTK.extract(features=["a_bry_ps"])
    return extracted_features["a_bry_ps"]

def num_pos(text,nlp):
    list_num_pos = []
    sentences = sent_tokenize(text)
    for sentence in sentences:
        doc = nlp(sentence)
        pos_list = []
        for token in doc:
            pos_list.append(token.pos_)
        uniq_pos = len(Counter(pos_list).keys())
        list_num_pos.append(uniq_pos)
    return sum(list_num_pos)

def avg_num_pos(text,nlp):
    list_num_pos = []
    sentences = sent_tokenize(text)
    for sentence in sentences:
        doc = nlp(sentence)
        pos_list = []
        for token in doc:
            pos_list.append(token.pos_)
        uniq_pos = len(Counter(pos_list).keys())
        list_num_pos.append(uniq_pos)
    return sum(list_num_pos)/len(list_num_pos)

# old and not used
# def avg_GPCs_per_word(text,nlp):
#     g2p = G2p()
#     num_of_gpc = len(g2p(text))
#     doc = nlp(text)
#     LFTK = lftk.Extractor(docs=doc)
#     extracted_features = LFTK.extract(features=["t_word"])
#     num_of_words = extracted_features['t_word']
#     return num_of_gpc/num_of_words
#
# def uniq_GPCs(text):
#     list_of_gpc = []
#     sentences = sent_tokenize(text)
#     g2p = G2p()
#     for sentence in sentences:
#         num_of_gpc = len(g2p(sentence))
#         list_of_gpc.append(num_of_gpc)
#     return sum(list_of_gpc)
#
# def avg_uniq_GPCs(text):
#     list_of_gpc = []
#     sentences = sent_tokenize(text)
#     g2p = G2p()
#     for sentence in sentences:
#         num_of_gpc = len(g2p(sentence))
#         list_of_gpc.append(num_of_gpc)
#     return sum(list_of_gpc)/len(list_of_gpc)
#
# def avg_phonemes_per_word(text):
#     list_of_gpc = []
#     g2p = G2p()
#     words = word_tokenize(text)
#     for word in words:
#         num_of_gpc = len(g2p(word))
#         list_of_gpc.append(num_of_gpc)
#     return sum(list_of_gpc)/len(list_of_gpc)

def clean_text(text):
    # Convert text to lowercase
    text = text.lower()

    # Remove non-alphabetical characters using regular expressions
    text = re.sub(r'[^a-z]', ' ', text)

    # Remove extra spaces
    text = ' '.join(text.split())
    return text

def avg_GPCs_per_word(text_to_process):

    text_to_process = clean_text(text_to_process)

    # Command to run the other script with the text as an argument
    command = ["python3", "trained_models/linguistic_features/run_phonemes_graphemes_alignment.py", text_to_process]

    result = subprocess.run(command, capture_output=True, text=True)

    # Access the standard output of the called script
    output_from_called_script = result.stdout
    return float(output_from_called_script.strip())


def avg_l_s_d (text):
    text = clean_text(text)
    list_of_lsd = []
    g2p = G2p()
    words = word_tokenize(text)
    for word in words:
        num_of_phonemes = len(g2p(word))
        num_of_letters = len(word)
        list_of_lsd.append(abs(num_of_letters-num_of_phonemes))
    return sum(list_of_lsd)/len(list_of_lsd)


