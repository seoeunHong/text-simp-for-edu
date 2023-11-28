from trained_models.linguistic_features import linguistic_textual_features
from trained_models.linguistic_features import readability_formulas_functions
from trained_models.linguistic_features import linguistic_formulas_features

def syntax_complexity_all(text,nlp):
    # Given a text, return the scores for all readability formulas and additional linguistic textual features from the syntax complexity category
    Flesch_reading_ease = readability_formulas_functions.Flesch_reading_ease(text)
    Flesch_Kincaid = readability_formulas_functions.Flesch_Kincaid(text)
    Automated_readability_index = readability_formulas_functions.Automated_readability_index(text)
    Coleman_Liau_index = readability_formulas_functions.Coleman_Liau_index(text)

    parsing_tree_depth = linguistic_textual_features.parsing_tree_depth(text, nlp)
    max_nesting_level = linguistic_textual_features.max_nesting_level(text, nlp)
    punctiations_num = linguistic_textual_features.puntuations_num(text, nlp)
    num_entity = linguistic_textual_features.num_of_entity(text, nlp)

    syntax_complexity_dict = {
        'Flesch reading ease grade': Flesch_reading_ease,
        'Flesch Kincaid grade': Flesch_Kincaid,
        'Automated readability index grade': Automated_readability_index,
        'Coleman Liau Index grade': Coleman_Liau_index,

        'parsing tree depth': parsing_tree_depth,
        'max nesting level': max_nesting_level,
        'puntuations num': punctiations_num,
        'num entity': num_entity,
    }
    return syntax_complexity_dict

def syntax_complexity_chosen(text,nlp):
    # Same as above but retaining only those matrices that differed between classes (interesting features)
    Flesch_Kincaid = readability_formulas_functions.Flesch_Kincaid(text)
    Automated_readability_index = readability_formulas_functions.Automated_readability_index(text)
    Coleman_Liau_index = readability_formulas_functions.Coleman_Liau_index(text)

    parsing_tree_depth = linguistic_textual_features.parsing_tree_depth(text, nlp)
    max_nesting_level = linguistic_textual_features.max_nesting_level(text, nlp)

    syntax_complexity_dict = {
        'Flesch Kincaid grade': Flesch_Kincaid,
        'Automated readability index grade': Automated_readability_index,
        'Coleman Liau Index grade': Coleman_Liau_index,

        'parsing tree depth': parsing_tree_depth,
        'max nesting level': max_nesting_level,
    }
    return syntax_complexity_dict

def lexical_complexity_all(text, nlp):
    # Given a text, return the scores for all readability formulas and additional linguistic textual features from the lexical complexity category

    smog = readability_formulas_functions.smog(text)
    Dale_Chall = readability_formulas_functions.Dale_Chall(text)
    Linsear_Write = readability_formulas_functions.Linsear_Write(text)
    Gunning_Fog_Index = readability_formulas_functions.gunning_fog_index(text)

    num_pos = linguistic_textual_features.num_pos(text,nlp)
    kup_AoA = linguistic_textual_features.kuperman_AoA(text,nlp)
    bry_AoA = linguistic_textual_features.brysbaer_AoA(text,nlp)

    lexical_complexity_dict = {
        'smog grade': smog,
        'Dale Chall grade': Dale_Chall,
        'Linsear Write grade': Linsear_Write,
        'Gunning Fog Index grade': Gunning_Fog_Index,

        'num of POS': num_pos,
        'kuperman AoA': kup_AoA,
        'brysbaert AoA': bry_AoA,
    }
    return lexical_complexity_dict

def lexical_complexity_chosen(text,nlp):
    # Same as above but retaining only those matrices that differed between classes (interesting features)
    Dale_Chall = readability_formulas_functions.Dale_Chall(text)
    Linsear_Write = readability_formulas_functions.Linsear_Write(text)

    kup_AoA = linguistic_textual_features.kuperman_AoA(text,nlp)

    lexical_complexity_dict = {
        'Dale Chall grade': Dale_Chall,
        'Linsear Write grade': Linsear_Write,
        'kuperman AoA': kup_AoA,
    }
    return lexical_complexity_dict

def decodability_all(text,nlp):
    # Given a text, return the scores for all readability formulas and additional linguistic textual features from the decodability complexity category

    avg_GPCs_per_word = linguistic_textual_features.avg_GPCs_per_word(text,nlp)
    avg_uniq_GPCs_per_sentence = linguistic_textual_features.uniq_GPCs(text)
    decodability_dict = {
        'avg GPCs per word': avg_GPCs_per_word,
        'avg uniq GPCs per sentence': avg_uniq_GPCs_per_sentence}
    return decodability_dict

def decodability_chosen(text,nlp):
    # Same as above but retaining only those matrices that differed between classes (interesting features)
    avg_uniq_GPCs_per_sentence = linguistic_textual_features.uniq_GPCs(text)
    decodability_dict = {
        'avg uniq GPCs per sentence': avg_uniq_GPCs_per_sentence}
    return decodability_dict

def all_readability_formulas(text,nlp):
    # Given a text, return the scores for all readability formulas
    Flesch_reading_ease = readability_formulas_functions.Flesch_reading_ease(text)
    Flesch_Kincaid = readability_formulas_functions.Flesch_Kincaid(text)
    Automated_readability_index = readability_formulas_functions.Automated_readability_index(text)
    Coleman_Liau_index = readability_formulas_functions.Coleman_Liau_index(text)
    smog = readability_formulas_functions.smog(text)
    Dale_Chall = readability_formulas_functions.Dale_Chall(text)
    Linsear_Write = readability_formulas_functions.Linsear_Write(text)
    Gunning_Fog_Index = readability_formulas_functions.gunning_fog_index(text)

    readability_formulas_dict = {
        'Flesch reading ease grade': Flesch_reading_ease,
        'Flesch Kincaid grade': Flesch_Kincaid,
        'Automated readability index grade': Automated_readability_index,
        'Coleman Liau Index grade': Coleman_Liau_index,
        'smog grade': smog,
        'Dale Chall grade': Dale_Chall,
        'Linsear Write grade': Linsear_Write,
        'Gunning Fog Index grade': Gunning_Fog_Index}

    return readability_formulas_dict


def syntax_linguistic_features(text, nlp):
    # Same as above but only the linguistic textual features that are based on syntax.
    # This is the final set of features used for predicting Lexile scores according to syntax.

    avg_words_in_text = linguistic_formulas_features.avg_words_in_text(text)
    avg_num_of_characters = linguistic_formulas_features.avg_num_of_characters(text)

    parsing_tree_depth = linguistic_textual_features.parsing_tree_depth(text, nlp)
    max_nesting_level = linguistic_textual_features.max_nesting_level(text, nlp)
    avg_puncuations_num = linguistic_textual_features.avg_puncuations_num(text, nlp)
    avg_num_of_entity = linguistic_textual_features.avg_num_of_entity(text, nlp)
    avg_num_pos = linguistic_textual_features.avg_num_pos(text, nlp)


    avg_syntax_linguistic_features_dict = {
        'avg words in text': avg_words_in_text,
        'avg num of charachters': avg_num_of_characters,
        'avg parsing tree depth': parsing_tree_depth,
        'avg max nesting level': max_nesting_level,
        'avg puncuations num': avg_puncuations_num,
        'avg num of entity': avg_num_of_entity,
        'avg num of POS': avg_num_pos
    }

    return avg_syntax_linguistic_features_dict

def lexical_linguistic_features(text, nlp):
    # Same as above but only the linguistic textual features that are based on lexical.
    # This is the final set of features used for predicting Lexile scores according to lexical.

    avg_DallChall_words = linguistic_formulas_features.avg_DallChall_words(text)
    avg_syllables_in_text = linguistic_formulas_features.avg_syllables_in_text(text)
    avg_difficult_words_acc_syllabels = linguistic_formulas_features.avg_difficult_words_acc_syllabels(text)

    kuperman_AoA = linguistic_textual_features.kuperman_AoA(text, nlp)

    avg_lexical_linguistic_features_dict = {
        'avg DallChall words in text': avg_DallChall_words,
        'avg syllables in text': avg_syllables_in_text,
        'avg difficult words acc syllabels': avg_difficult_words_acc_syllabels,
        'avg kuperman AoA': kuperman_AoA,
    }
    return avg_lexical_linguistic_features_dict

def decodability_linguistic_features(text, nlp):
    # Same as above but only the linguistic textual features that are based on decodability.
    # This is the final set of features used for predicting Lexile scores according to decodability.

    trr = linguistic_formulas_features.ttr(text)
    avg_l_s_d = linguistic_textual_features.avg_l_s_d(text)
    avg_GPCs_per_word = linguistic_textual_features.avg_GPCs_per_word(text)

    avg_decodability_linguistic_features_dict = {
        'ttr': trr,
        'avg l_s_d': avg_l_s_d,
        'avg GPCs per word': avg_GPCs_per_word
    }
    return avg_decodability_linguistic_features_dict

def all_linguistic_features(text,nlp):
    # Given a text, return the scores for all linguistic features
    # Taking into account all the linguistic textual features as before
    # But now instead of readability formulas, we take the linguistic features that the readability formulas are based on.

    avg_words_in_text = linguistic_formulas_features.avg_words_in_text(text)
    avg_num_of_characters = linguistic_formulas_features.avg_num_of_characters(text)
    parsing_tree_depth = linguistic_textual_features.parsing_tree_depth(text, nlp)
    max_nesting_level = linguistic_textual_features.max_nesting_level(text, nlp)
    avg_puncuations_num = linguistic_textual_features.avg_puncuations_num(text, nlp)
    avg_num_of_entity = linguistic_textual_features.avg_num_of_entity(text, nlp)
    avg_num_pos = linguistic_textual_features.avg_num_pos(text, nlp)

    avg_DallChall_words = linguistic_formulas_features.avg_DallChall_words(text)
    avg_syllables_in_text = linguistic_formulas_features.avg_syllables_in_text(text)
    avg_difficult_words_acc_syllabels = linguistic_formulas_features.avg_difficult_words_acc_syllabels(text)
    kuperman_AoA = linguistic_textual_features.kuperman_AoA(text, nlp)

    trr = linguistic_formulas_features.ttr(text)
    avg_l_s_d = linguistic_textual_features.avg_l_s_d(text)
    avg_GPCs_per_word = linguistic_textual_features.avg_GPCs_per_word(text)

    all_features_dict = {
        'avg words in text': avg_words_in_text,
        'avg num of charachters': avg_num_of_characters,
        'avg parsing tree depth': parsing_tree_depth,
        'avg max nesting level': max_nesting_level,
        'avg puncuations num': avg_puncuations_num,
        'avg num of entity': avg_num_of_entity,
        'avg num of POS': avg_num_pos,
        'avg DallChall words in text': avg_DallChall_words,
        'avg syllables in text': avg_syllables_in_text,
        'avg difficult words acc syllabels': avg_difficult_words_acc_syllabels,
        'avg kuperman AoA': kuperman_AoA,
        'ttr': trr,
        'avg l_s_d': avg_l_s_d,
        'avg GPCs per word': avg_GPCs_per_word
    }

    return all_features_dict











