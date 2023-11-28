import json
from nltk.tokenize import sent_tokenize, word_tokenize
from g2p_en import G2p
import sys

import numpy as np
from itertools import combinations_with_replacement
import os
path = os.path.abspath("my_log")
sys.path.append(path)
from my_log import logging

def load_transcription(transcription_file_name):
    """
    :return: a list of tuple:
        [
        (word: string, phones: list),
        (word: string, phones: list),
        ...,
        (word: string, phones: list),
        ]
    """
    transcription_list = list()
    with open(transcription_file_name, "r") as transcription_file:
        while 1:
            lines = transcription_file.readlines(10000)
            if not lines:
                break
            for line in lines:
                line = line.strip()
                word = line.split("\t")[0]
                phones = line.split("\t")[1].split(" ")
                transcription_list.append((word, phones))
                pass
        pass
        transcription_list = transcription_list
        logging.debug("transcription_list:")
        logging.debug(transcription_list)
        return transcription_list


def load_grapheme_dict(transcription_list):
    """
    :return: a dictionary of grapheme-id pair like: {"a": 0, "b": 1, "c": 2, ...,}
    """
    grapheme_set = set()
    for (word, _) in transcription_list:
        grapheme_set = grapheme_set.union(word)
        pass
    grapheme_list = list(grapheme_set)
    grapheme_dict = dict()
    for i in range(len(grapheme_list)):
        grapheme_dict[grapheme_list[i]] = i
        pass
    grapheme_dict = grapheme_dict
    logging.debug("grapheme_dict:")
    logging.debug(grapheme_dict)
    return grapheme_dict


def load_phoneme_dict(transcription_list):
    """
    :return: a dictionary of phoneme-id pair like: {"ey1":0, "b":1, "iy2": 2, "s": 3, "iy2": 4, ...,}
    """
    phoneme_set = set()
    for (_, phones) in transcription_list:
        phoneme_set = phoneme_set.union(phones)
        pass
    phoneme_list = list(phoneme_set)
    phoneme_list.append("*")
    phoneme_dict = dict()
    for i in range(len(phoneme_list)):
        phoneme_dict[phoneme_list[i]] = i
        pass
    phoneme_dict = phoneme_dict
    logging.debug("phoneme_dict:")
    logging.debug(phoneme_dict)
    return phoneme_dict


def introduce_epsilon_phone_seq(word, phones):
    """
    Introduce epsilon to every possible location in phones list.
    :param word:
    :param phones:
    :return: a list containing all word-phones pairs with epsilon introduced
    """
    length_diff = len(word) - len(phones)
    if length_diff < 0:
        logging.error("Word length is less than phones'!")
        logging.info(word + "-" + str(phones))
    location_combines_with_replace = [c for c in combinations_with_replacement(range(len(phones) + 1), length_diff)]
    pair_list = list()
    for locations in location_combines_with_replace:
        temp_phones = phones.copy()
        for i in range(len(locations)):
            temp_phones.insert(locations[i] + i, "*")
            pass
        pair_list.append((word, temp_phones))
        pass
    return pair_list


def is_prob_matrix_equal(last_prob_matrix, new_prob_matrix, epsilon):
    """
    :param last_prob_matrix: numpy array.
    :param new_prob_matrix: numpy array.
    :param epsilon:
    :return: True: if mean-square error <= epsilon
                False: if mean-square error > epsilon
    """
    diff_mean = np.mean(np.subtract(last_prob_matrix, new_prob_matrix))
    if diff_mean <= epsilon:
        return True
    return False


def path_to_string(path_list):
    """
    :param path_list: a list of dtw path result, like:
        [
        ("a", "ey1"),
        ("b", "b_iy1"),
        ("c", "s_iy1"),
        ]
    :return: a string to be writen to the output file, like:
        abc ey1 b_iy1 s_iy1
    """
    word_list = []
    phones = []
    for step_tuple in path_list:
        word_list.append(step_tuple[0])
        phones.append(step_tuple[1])
        pass
    result = "".join(word_list) + "\t" + " ".join(phones) + "\n"
    return result


class Aligner:

    def __init__(self, training_file_name, test_data_file_name):
        self.training_data_file_name = training_file_name
        self.test_data_file_name = test_data_file_name
        self.transcription_list = list()
        self.grapheme_dict = dict()
        self.phoneme_dict = dict()
        self.prob_matrix = np.zeros(shape=(1, 1))
        pass

    def init_prob_matrix(self):
        """
        :return: matrix containing probabilities of a grapheme match a phoneme, initialized with 0 value.
        """
        g_count = len(self.grapheme_dict)
        p_count = len(self.phoneme_dict)
        self.prob_matrix = np.zeros(shape=(g_count, p_count), dtype=np.float32)
        logging.debug("prob_matrix:")
        logging.debug(self.prob_matrix)
        return self.prob_matrix

    def reset_prob_matrix(self, align_paths):
        """
        Reset prob matrix according to align paths.
        :param align_paths: a list of step lists, like:
            [
                [
                    ("a", "ey1"),
                    ("b", "b_iy1"),
                    ...,
                    ("c", "s_iy1"),
                ],
                [
                    ("a", "ey1"),
                    ("b", "b_iy1"),
                    ...,
                    ("c", "s_iy1"),
                ],
                ...,
                [
                    ("a", "ey1"),
                    ("b", "b_iy1"),
                    ...,
                    ("c", "s_iy1"),
                ],
            ]
        :return: prob matrix
        """
        logging.debug("before reset prob matrix:")
        logging.debug(self.prob_matrix)
        for align_path in align_paths:
            for step in align_path:
                g_id = self.get_grapheme_id(step[0])
                p_id = self.get_phoneme_id(step[1])
                self.prob_matrix[g_id][p_id] += 1
                pass
            pass
        self.normalize_prob_matrix()
        logging.debug("after reset prob matrix:")
        logging.debug(self.prob_matrix)
        return self.prob_matrix

    def normalize_prob_matrix(self):
        """
        Probability matrix is a matrix with shape: (grapheme_count, phoneme_count).
        Normalization is to keep sum of each row in the matrix to 1.
        :return: a normalized probability matrix.
        """
        shape = self.prob_matrix.shape
        sum_array = np.sum(self.prob_matrix, axis=1)
        for i in range(shape[0]):
            for j in range(shape[1]):
                self.prob_matrix[i][j] /= sum_array[i]
                pass
            pass
        logging.debug("prob_matrix:")
        logging.debug(self.prob_matrix)
        return self.prob_matrix

    def get_grapheme_id(self, grapheme):
        g_id = self.grapheme_dict[grapheme]
        return g_id

    def get_phoneme_id(self, phoneme):
        p_id = self.phoneme_dict[phoneme]
        return p_id

    def distance(self, grapheme, phoneme):
        """
        Calculate the distance(match probability) between a grapheme and a phoneme.
        :param grapheme: a string like: a
        :param phoneme: a string like: ey1
        :return: probability of grapheme match phoneme
        """
        g_id = self.get_grapheme_id(grapheme)
        p_id = self.get_phoneme_id(phoneme)
        distance = self.prob_matrix[g_id][p_id]
        return distance

    def init_prob_of_grapheme_match_phoneme(self):
        """
        Initialize prob_matrix: the probability of G matching P, counting with DTW all possible G/P association for all possible epsilon positions in the phonetic
        :return: prob_matrix
        """
        self.transcription_list = load_transcription(training_data_file_name)
        self.grapheme_dict = load_grapheme_dict(self.transcription_list)
        self.phoneme_dict = load_phoneme_dict(self.transcription_list)
        self.init_prob_matrix()
        align_paths = []
        for (word, phones) in self.transcription_list:
            pair_list = introduce_epsilon_phone_seq(word, phones)  # Introduce epsilon into phone list
            for (w, p) in pair_list:
                # align_path, _ = self.dynamic_time_wrapping(w, p)
                align_path = []
                for i in range(len(w)):
                    align_path.append((w[i], p[i]))
                align_paths.append(align_path)
            pass
        self.reset_prob_matrix(align_paths)
        return self.prob_matrix

    def dynamic_time_wrapping(self, word, phones):
        """
        Dynamic time wrapping for word-phones pair.
        :param word: a string represent a word
        :param phones: a list of string represent some phones
        :return: a list of tuple represent the best path, like:
            [
            ("a", "ey1"),
            ("b", "b_iy1"),
            ...,
            ("c", "s_iy1"),
            ]
        """
        g_count = len(word)
        p_count = len(phones)
        frame_dist_matrix = np.zeros(shape=(g_count, p_count), dtype=np.float32)  # Frame distance matrix.
        for i in range(g_count):
            for j in range(p_count):
                frame_dist_matrix[i][j] = self.distance(word[i], phones[j])
                pass
            pass
        acc_dist_matrix = np.zeros(shape=(g_count, p_count), dtype=np.float32)  # Accumulated distance matrix.
        acc_dist_matrix[0][0] = frame_dist_matrix[0][0]
        """Dynamic programming to compute the accumulated probability."""
        for i in range(1, g_count):
            for j in range(p_count):
                d1 = acc_dist_matrix[i-1][j]
                if j > 0:
                    d2 = acc_dist_matrix[i-1][j-1]
                else:
                    d2 = 0
                acc_dist_matrix[i][j] = frame_dist_matrix[i][j] + max([d1, d2])
                pass
            pass
        prob_value = acc_dist_matrix[g_count-1][p_count-1]
        """Trace back to find the best path with the max accumulated probability."""
        align_path = []
        i, j = g_count-1, p_count-1
        while 1:
            align_path.append((word[i], phones[j]))
            if i == 0 & j == 0:
                break
            if i > 0:
                d1 = acc_dist_matrix[i - 1][j]
                if j > 0:
                    d2 = acc_dist_matrix[i - 1][j - 1]
                else:
                    d2 = 0
            else:
                d1 = 0
                d2 = 0
            candidate_steps = [(i-1, j), (i-1, j-1)]
            candidate_prob = [d1, d2]
            i, j = candidate_steps[candidate_prob.index(max(candidate_prob))]
            pass
        align_path.reverse()
        return align_path, prob_value

    def e_step(self):
        """
        Expectation step that computes a optimized path with maximum probability for each word-phones pair.
        :return: a list of align paths, like:
            [
                [("a", "ey1"), ("b", "b_iy10), ("c", "s_iy0"), ],
                [("a", "ey1"), ("b", "b_iy10), ],
                [("a", "ey1"), ("b", "b_iy10), ("c", "s_iy0"),  ],
                [("a", "ey1"), ("b", "b_iy10), ("c", "s_iy0"),  ("d", "d_iy0"), ],
            ]
        """
        align_paths = []
        for (word, phones) in self.transcription_list:
            pair_list = introduce_epsilon_phone_seq(word, phones)
            logging.debug("pair list:")
            logging.debug(pair_list)
            candidate_path_list = []  # Construct a candidate path list for all word-phones
            for (w, p) in pair_list:
                align_path, prob_value = self.dynamic_time_wrapping(w, p)
                candidate_path_list.append((align_path, prob_value))
            candidate_path_list.sort(key=lambda x: x[1], reverse=True)  # Sort by probability
            align_paths.append(candidate_path_list[0][0])  # Pick up the promising path with the biggest probability.
            pass
        return align_paths

    def m_step(self, align_paths):
        """
        Maximum likelihood step that resets the frame prob matrix according to align paths generated by e_step.
        :param align_paths: a list of align paths generated by e_step function.
        """
        self.reset_prob_matrix(align_paths)
        pass

    def train(self, iter_num, epsilon):
        """
        Train prop matrix until iter_num or the difference of adjacent iteration results is no more than epsilon.
        :param iter_num:
        :param epsilon:
        """
        self.init_prob_of_grapheme_match_phoneme()
        for i in range(iter_num):
            logging.info("Training epoch:" + str(i))
            last_prob_matrix = self.prob_matrix.copy()
            align_paths = self.e_step()  # Expectation step
            self.m_step(align_paths)  # Maximum step
            # if self.is_prob_matrix_equal(last_prob_matrix, self.prob_matrix, epsilon):
            #     break
            pass
        pass

    def align(self):
        """
        Align the test data file by current model(frame prob matrix) trained already.
        :return:
        """
        transcription_list = load_transcription(self.test_data_file_name)
        result_list = []
        for (word, phones) in transcription_list:
            pair_list = introduce_epsilon_phone_seq(word, phones)
            candidate_path_list = []  # Construct a candidate path list for all possible word-phones pairs
            for (w, p) in pair_list:
                align_path, prob_value = self.dynamic_time_wrapping(w, p)
                candidate_path_list.append((align_path, prob_value))
            candidate_path_list.sort(key=lambda x: x[1], reverse=True)  # Sort by probability
            result_string = path_to_string(candidate_path_list[0][0])
            result_list.append(result_string)  # Pick up the promising path with the biggest probability.
        with open(output_file_name, "w") as output_file:
            output_file.writelines(result_list)
            pass
        pass
    pass

    def save_trained_model(self, model_file_name):
        """
        Save the trained model to a JSON file.
        :param model_file_name: Filename to save the model.
        """
        with open(model_file_name, "w") as model_file:
            model_data = {
                "grapheme_dict": self.grapheme_dict,
                "phoneme_dict": self.phoneme_dict,
                "prob_matrix": self.prob_matrix.tolist(),
            }
            json.dump(model_data, model_file, indent=4)

    @classmethod
    def load_trained_model(cls, model_file_name):
        """
        Load a trained model from a JSON file.
        :param model_file_name: Filename of the saved model.
        :return: An instance of Aligner with the loaded model.
        """
        with open(model_file_name, "r") as model_file:
            model_data = json.load(model_file)

        loaded_aligner = cls(training_data_file_name, test_data_file_name)
        loaded_aligner.grapheme_dict = model_data["grapheme_dict"]
        loaded_aligner.phoneme_dict = model_data["phoneme_dict"]
        loaded_aligner.prob_matrix = np.array(model_data["prob_matrix"])

        return loaded_aligner

def calculate_avg_word_GPCs_complexity(graphemes_phonemes_file):
    debug = 3
    with open("trained_models/linguistic_features/gpcs/grapheme_phoneme_probabilities.json", "r") as json_file:
        grapheme_phoneme_dict = json.load(json_file)

    with open(graphemes_phonemes_file, 'r') as file:
        lines = file.readlines()
        probs = []
        for line in lines:
            prob = 1
            line = line.strip().split('\t')  # Split the line into grapheme and phonemes
            graphemes = [char for char in line[0]]
            phonemes = line[1].split()  # Split the phonemes into a list

            for g, p in zip(graphemes, phonemes):
                # Initialize an empty dictionary for the grapheme if it doesn't exist
                if g not in grapheme_phoneme_dict:
                    prob = 0

                # Update the dictionary with the phoneme and its count
                if p in grapheme_phoneme_dict[g]:
                    prob = prob * grapheme_phoneme_dict[g][p]
                else:
                    prob = 0
            probs.append(prob)
        return sum(probs)/len(probs)


if __name__ == '__main__':
    # text = "a soft knock on the door made me"
    if len(sys.argv) != 2:
        print("Usage: python run_phonemes_graphemes_alignment.py <text>")
        sys.exit(1)

    text = sys.argv[1]

    g2p = G2p()
    output_file = "trained_models/linguistic_features/gpcs/phoneme_output.txt"

    word_list = word_tokenize(text)
    with open("trained_models/linguistic_features/gpcs/garbage_for_calculations/phonemes_dirty.txt", 'w') as file:
        for word in word_list:
            if not all(char.isalpha() for char in word):
                continue
            phoneme = ' '.join(g2p(word))
            line = f"{word}\t{phoneme}\n"
            file.write(line)


    file_name_before_clean = "trained_models/linguistic_features/gpcs/garbage_for_calculations/phonemes_dirty.txt"
    file_name_after_clean = "trained_models/linguistic_features/gpcs/garbage_for_calculations/phonemes_clean.txt"

    # Open the input file for reading
    with open(file_name_before_clean, "r") as original_file:
        # Open the output file for writing
        with open(file_name_after_clean, "w") as filtered_file:
            # Read and write the first 500,000 lines
            for line in original_file:
                # Split the line into word and phoneme parts
                word, phonemes = line.strip().split('\t')
                # Check if the length of the word is greater than or equal to the number of phonemes
                if len(word) >= len(phonemes.split()) and len(word)<12:
                    # If so, write the line to the filtered file
                    filtered_file.write(line)



    training_data_file_name = "trained_models/linguistic_features/gpcs/phonemes_train_ready_1000000.txt"
    test_data_file_name = "trained_models/linguistic_features/gpcs/garbage_for_calculations/phonemes_clean.txt"
    output_file_name = "trained_models/linguistic_features/gpcs/garbage_for_calculations/graphemes_phonemes.txt"
    with open(output_file_name, "w") as output_file:
        output_file.writelines(output_file_name)
    iter_num = 5
    epsilon = 0

    try:
        aligner = Aligner.load_trained_model("trained_models/linguistic_features/gpcs/Aligner_model_1000000.json")
    except FileNotFoundError:
        # If the trained model doesn't exist, train and save it
        aligner = Aligner(training_data_file_name, test_data_file_name)
        aligner.train(iter_num, epsilon)
        aligner.save_trained_model("trained_models/linguistic_features/gpcs/Aligner_model_not_found.json")
        # Perform alignment using the trained model
    aligner.align()

    print(calculate_avg_word_GPCs_complexity(output_file_name))












