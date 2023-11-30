from datasets import load_dataset
from nltk.tokenize import sent_tokenize
import statistics
import pandas as pd
import numpy as np

def mean_num_of_sentences(data_path):
    # This function calculates the average number of sentences for each question in the Datasets.
    # This information will be used to split the text into x sentences so that the linear regression can be trained on data that is as similar as possible to the true data
    ny_state_math = load_dataset(data_path)["train"]
    question_column = ny_state_math["question"]
    sentences_per_question = [len(sent_tokenize(question)) for question in question_column]
    mean_sentences = statistics.mean(sentences_per_question)
    return round(mean_sentences)+2

def split_text_into_parts(text, sentences_per_part):
    # This function divides a text into parts containing x sentences each.
    # However, it is no longer necessary as the features used are calculated by averaging scores over the sentences, making the text length irrelevant.
    sentences = sent_tokenize(text)
    num_sentences = len(sentences)
    parts = [sentences[i:i + sentences_per_part] for i in range(0, num_sentences, sentences_per_part)]
    return [' '.join(part) for part in parts]

def read_xlsx_to_df(dataset_path):
    df = pd.read_excel(dataset_path)
    return df

def read_xlsx_to_x_sentences_df(dataset_path, num_of_sentences):
    # The function returns a DataFrame with all the information, but with the texts split into x sentences each.
    # This functionality is no longer necessary.
    df = pd.read_excel(dataset_path)
    df_original_columns = df.columns
    new_df = pd.DataFrame(columns=df_original_columns)
    for index, row in df.iterrows():
        parts = split_text_into_parts(row["Content"], num_of_sentences)
        for part in parts:
            dict_format = {'Title': row['Title'],'Content': part,'Lexile':row['Lexile'], 'Grade': row['Grade']}
            new_df = pd.concat([new_df, pd.DataFrame([dict_format])], ignore_index=True)
    return new_df

def Lexile_group_5(lexile, percentile_20, percentile_40, percentile_60, percentile_80):
    # The function divides the texts in the database into five groups,
    # with one-fifth of the examples having the lowest scores assigned to group one,
    # and similarly, one-fifth of the examples with the highest scores assigned to group five.
    if lexile < percentile_20:
        return 1
    elif lexile < percentile_40:
        return 2
    elif lexile < percentile_60:
        return 3
    elif lexile < percentile_80:
        return 4
    else:
        return 5

def add__group(dataset_path):
    # This function adds a Lexile group to the datasets while removing rows with null values.
    df = pd.read_excel(dataset_path)
    df = df[df['Lexile'] != "Lexile not found"]
    percentile_20 = np.percentile(df['Lexile score'], 20)
    percentile_40 = np.percentile(df['Lexile score'], 40)
    percentile_60 = np.percentile(df['Lexile score'], 60)
    percentile_80 = np.percentile(df['Lexile score'], 80)
    df['Lexile group'] = df['Lexile score'].apply(lambda x: Lexile_group_5(x, percentile_20, percentile_40, percentile_60,percentile_80 ))
    output_file = 'Datasets/Lexile_dataset.xlsx'
    df.to_excel(output_file, index=False)  # Set index=False to exclude index column

# if __name__ == '__main__':
#     dataset_path = 'Datasets/Lexile_dataset.xlsx'
#     add_Lexile_value_and_group(dataset_path)

