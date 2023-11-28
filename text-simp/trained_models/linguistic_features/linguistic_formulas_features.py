from nltk.stem import PorterStemmer
from nltk.tokenize import word_tokenize
import re
import syllables

stemmer = PorterStemmer()  # Initialize the Porter Stemmer

def build_DallChall_dict():
    DallChall_dict = {}
    with open('trained_models/linguistic_features/Datasets/Dale-Chall.txt', 'r') as file:
        current_heading = None  # Initialize the current heading
        for line in file:
            line = line.strip()  # Remove leading/trailing whitespace
            if not line:
                continue  # Skip empty lines
            # Check if the line starts with an alphabetical character (indicating a heading)
            if line.isalpha():
                current_heading = line  # Update the current heading
                DallChall_dict[current_heading] = []  # Initialize an empty list for words under this heading
            else:
                words = word_tokenize(line)  # Tokenize the line into words
                stemmed_words = [stemmer.stem(word) for word in words]  # Stem the words
                if current_heading:
                    DallChall_dict[current_heading].extend(stemmed_words)
    return DallChall_dict

def DallChall_words(text):
    DallChall_dict = build_DallChall_dict()
    word_count = 0
    words = text.split()
    for word in words:
        # Stem the word using the same Porter Stemmer
        stemmed_word = stemmer.stem(word)
        # Iterate through the DallChall_dict
        for heading, words_under_heading in DallChall_dict.items():
            # Check if the stemmed word is in the list of words under the current heading
            if stemmed_word in words_under_heading:
                word_count += 1  # Increment the word count
    return word_count

def avg_DallChall_words(text):
    DallChall_dict = build_DallChall_dict()
    word_count = 0
    words = text.split()
    for word in words:
        # Stem the word using the same Porter Stemmer
        stemmed_word = stemmer.stem(word)
        # Iterate through the DallChall_dict
        for heading, words_under_heading in DallChall_dict.items():
            # Check if the stemmed word is in the list of words under the current heading
            if stemmed_word in words_under_heading:
                word_count += 1  # Increment the word count
    sentences = re.split(r'[.!?]', text)
    sentences = [sentence.strip() for sentence in sentences if sentence.strip()]
    return word_count/len(sentences)

def words_in_text(text):
    words = text.split()
    return len(words)

def avg_words_in_text(text):
    words = text.split()
    sentences = re.split(r'[.!?]', text)
    sentences = [sentence.strip() for sentence in sentences if sentence.strip()]
    return len(words)/len(sentences)

def syllables_in_text(text):
    words = text.split()
    count = 0
    for word in words:
        count += syllables.estimate(word)
    return count

def avg_syllables_in_text(text):
    words = text.split()
    count = 0
    for word in words:
        count += syllables.estimate(word)
    sentences = re.split(r'[.!?]', text)
    sentences = [sentence.strip() for sentence in sentences if sentence.strip()]
    return count/len(sentences)

def difficult_words_acc_syllabels(text):
    words = text.split()
    count = 0
    for word in words:
        if syllables.estimate(word) > 2:
            count += 1
    return count

def avg_difficult_words_acc_syllabels(text):
    words = text.split()
    count = 0
    for word in words:
        if syllables.estimate(word) > 2:
            count += 1
    sentences = re.split(r'[.!?]', text)
    sentences = [sentence.strip() for sentence in sentences if sentence.strip()]
    return count/len(sentences)

def num_of_characters(text):
    alphanumeric_chars = re.findall(r'[a-zA-Z0-9]', text)
    return len(alphanumeric_chars)

def avg_num_of_characters(text):
    alphanumeric_chars = re.findall(r'[a-zA-Z0-9]', text)
    sentences = re.split(r'[.!?]', text)
    sentences = [sentence.strip() for sentence in sentences if sentence.strip()]
    return len(alphanumeric_chars)/len(sentences)

def ttr(text):
    words = text.split()
    total_tokens = len(words)
    word_set = set()
    for word in words:
        # Stem the word using the same Porter Stemmer
        stemmed_word = stemmer.stem(word)
        word_set.add(stemmed_word)
    total_unique_words = len(word_set)
    return total_unique_words / total_tokens



