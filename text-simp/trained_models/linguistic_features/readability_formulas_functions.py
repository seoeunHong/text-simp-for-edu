import textstat

def return_num(grade):
    translation_dict = {"4th grade or lower":4,"5th-or 6th-grade student":5,"7th-or 8th-grade student":7,
                        "9th-or 10th-grade student":9,"11th-or 12th-grade student":11,"college student":13,
                        "10th to 12th grade":10,"8th & 9th grade":8,"1th grade":1, "2th grade":2,
                        "3th grade":3,"4th grade":4, "5th grade":5,"6th grade":6, "7th grade":7,
                        "8th grade":8, "9th grade":9, "10th grade":10,"11th grade":11, "12th grade":12,
                        "2th grade or lower":2,"3th grade or lower":3, "5th grade or lower":5}
    return translation_dict[grade]


def Dale_Chall(text):
    # taking into account num difficult words (according to word list) and num of words in sentence(lower easier)
    Dale_Chall = textstat.dale_chall_readability_score(text)
    if Dale_Chall < 5:
        return return_num("4th grade or lower")
    elif Dale_Chall < 6:
        return return_num("5th-or 6th-grade student")
    elif Dale_Chall < 7:
        return return_num("7th-or 8th-grade student")
    elif Dale_Chall < 8:
        return return_num("9th-or 10th-grade student")
    elif Dale_Chall < 9:
        return return_num("11th-or 12th-grade student")
    # elif Dale_Chall >= 9:
    return return_num("college student")

def Flesch_reading_ease(text):
    # taking into account num of syllables, num of words, num of sentences (higher easier)
    Flesch_reading_ease = textstat.flesch_reading_ease(text)
    if Flesch_reading_ease < 50:
        return return_num("college student")
    elif Flesch_reading_ease < 60:
        return return_num("10th to 12th grade")
    elif Flesch_reading_ease < 70:
        return return_num("8th & 9th grade")
    elif Flesch_reading_ease < 80:
        return return_num("7th grade")
    elif Flesch_reading_ease < 90:
        return return_num("6th grade")
    # elif Flesch_reading_ease >= 90:
    return return_num("5th grade or lower")

def Flesch_Kincaid(text):
    # taking into account num of syllables, num of words, num of sentences (higher easier)
    Flesch_reading_ease = textstat.flesch_kincaid_grade(text)
    if Flesch_reading_ease < 3:
        return return_num("2th grade or lower")
    elif Flesch_reading_ease < 4:
        return return_num("3th grade")
    elif Flesch_reading_ease < 5:
        return return_num("4th grade")
    elif Flesch_reading_ease < 6:
        return return_num("5th grade")
    elif Flesch_reading_ease < 7:
        return return_num("6th grade")
    elif Flesch_reading_ease < 8:
        return return_num("7th grade")
    elif Flesch_reading_ease < 9:
        return return_num("8th grade")
    elif Flesch_reading_ease < 10:
        return return_num("9th grade")
    elif Flesch_reading_ease < 11:
        return return_num("10th grade")
    elif Flesch_reading_ease < 12:
        return return_num("11th grade")
    elif Flesch_reading_ease < 13:
        return return_num("12th grade")
    #elif Flesch_reading_ease >=13:
    return return_num("college student")

def gunning_fog_index(text):
    # taking into account num of words, num of polysyllables (words of 3 or more syllables), num of sentences (lower easier)
    Gunning_Fog_Index = textstat.gunning_fog(text)
    if Gunning_Fog_Index <= 3:
        return return_num("3th grade or lower")
    elif Gunning_Fog_Index <= 4:
        return return_num("4th grade")
    elif Gunning_Fog_Index <= 5:
        return return_num("5th grade")
    elif Gunning_Fog_Index <= 6:
        return return_num("6th grade")
    elif Gunning_Fog_Index <= 7:
        return return_num("7th grade")
    elif Gunning_Fog_Index <= 8:
        return return_num("8th grade")
    elif Gunning_Fog_Index <= 9:
        return return_num("9th grade")
    elif Gunning_Fog_Index <= 10:
        return return_num("10th grade")
    elif Gunning_Fog_Index <= 11:
        return return_num("11th grade")
    elif Gunning_Fog_Index <= 12:
        return return_num("12th grade")
    #elif Gunning_Fog_Index > 12:
    return return_num("college student")

def smog (text):
    # taking into account polysyllables (words of 3 or more syllables) and num of sentences (lower easier)
    SMOG = textstat.smog_index(text)
    if SMOG < 2:
        return return_num("1th grade")
    elif SMOG < 3:
        return return_num("2th grade")
    elif SMOG < 4:
        return return_num("3th grade")
    elif SMOG < 5:
        return return_num("4th grade")
    elif SMOG < 6:
        return return_num("5th grade")
    elif SMOG < 7:
        return return_num("6th grade")
    elif SMOG < 8:
        return return_num("7th grade")
    elif SMOG < 9:
        return return_num("8th grade")
    elif SMOG < 10:
        return return_num("9th grade")
    elif SMOG < 11:
        return return_num("10th grade")
    elif SMOG < 12:
        return return_num("11th grade")
    elif SMOG < 13:
        return return_num("12th grade")
    #elif SMOG > 13:
    return return_num("college student")

def Automated_readability_index(text):
    # taking into account num of characters, num of words, num of sentences (lower easier)
    ARI = textstat.automated_readability_index(text)
    if ARI <= 2:
        return return_num("1th grade")
    elif ARI <= 3:
        return return_num("2th grade")
    elif ARI <= 4:
        return return_num("3th grade")
    elif ARI <= 5:
        return return_num("4th grade")
    elif ARI <= 6:
        return return_num("5th grade")
    elif ARI <= 7:
        return return_num("6th grade")
    elif ARI <= 8:
        return return_num("7th grade")
    elif ARI <= 9:
        return return_num("8th grade")
    elif ARI <= 10:
        return return_num("9th grade")
    elif ARI <= 11:
        return return_num("10th grade")
    elif ARI <= 12:
        return return_num("11th grade")
    elif ARI <= 13:
        return return_num("12th grade")
    #elif ARI > 13:
    return return_num("college student")

def Coleman_Liau_index(text):
    # taking into account num of characters, num of words, num of sentences (lower easier)
    Coleman_Liau_index = textstat.coleman_liau_index(text)
    if Coleman_Liau_index < 3:
        return return_num("2th grade or lower")
    elif Coleman_Liau_index < 4:
        return return_num("3th grade")
    elif Coleman_Liau_index < 5:
        return return_num("4th grade")
    elif Coleman_Liau_index < 6:
        return return_num("5th grade")
    elif Coleman_Liau_index < 7:
        return return_num("6th grade")
    elif Coleman_Liau_index < 8:
        return return_num("7th grade")
    elif Coleman_Liau_index < 9:
        return return_num("8th grade")
    elif Coleman_Liau_index < 10:
        return return_num("9th grade")
    elif Coleman_Liau_index < 11:
        return return_num("10th grade")
    elif Coleman_Liau_index < 12:
        return return_num("11th grade")
    elif Coleman_Liau_index < 13:
        return return_num("12th grade")
    #elif Coleman_Liau_index >= 13:
    return return_num("college student")

def Linsear_Write(text):
    # taking into account num of words with x syllables, num of sentences (lower easier)
    Linsear_Write = textstat.linsear_write_formula(text)
    if Linsear_Write <2:
        return return_num("1th grade")
    if Linsear_Write <3:
        return return_num("2th grade")
    elif Linsear_Write <4:
        return return_num("3th grade")
    elif Linsear_Write <5:
        return return_num("4th grade")
    elif Linsear_Write <6:
        return return_num("5th grade")
    elif Linsear_Write <7:
        return return_num("6th grade")
    elif Linsear_Write <8:
        return return_num("7th grade")
    elif Linsear_Write <9:
        return return_num("8th grade")
    elif Linsear_Write <10:
        return return_num("9th grade")
    elif Linsear_Write <11:
        return return_num("10th grade")
    elif Linsear_Write <12:
        return return_num("11th grade")
    elif Linsear_Write <13:
        return return_num("12th grade")
    #elif Linsear_Write >=13:
    return return_num("college student")
