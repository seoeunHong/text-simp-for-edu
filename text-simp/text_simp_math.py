import openai
import os
import numpy as np
import pandas as pd
from datasets import load_dataset
from math_verifier import extract_question, is_solvable
from trained_models.final_model import calculate_text_score
from prompts import prompts_math
import re
import time

openai.api_key = os.getenv("OPENAI_API_KEY")
print('OPENAI API KEY: ', openai.api_key)

OPENAI_MODEL = "gpt-3.5-turbo"

def minimal_lexile_score(dataset_name, sampels_num, iterations_num, prompt_detail):
    experiment_df = pd.DataFrame(columns=["Id", "Given Text", "G Lexile","Answer","massage", "Simplified Text", "S Lexile","Solvable", "Iteration"])

    # upload the Datasets
    dataset = load_dataset(dataset_name, 'main')
    train_dataset = dataset["train"]

    for text_number in range(3, 3+sampels_num):
        id = text_number
        given_text = train_dataset[text_number]["question"]
        answer = train_dataset[text_number]["answer"]

        G_lexile = calculate_text_score(given_text, "lexile")
        messages = prompts_math.minimal_exp_initial_prompt(prompt_detail, given_text, G_lexile)

        for iteration in range(1,1+iterations_num):
            retry_count = 0
            success = False
            while retry_count < 3:  # Retry up to 3 times
                try:
                    response = openai.ChatCompletion.create(
                        model=OPENAI_MODEL,
                        messages=messages,
                        max_tokens=160,
                    )
                    success = True
                    break
                except:
                    print(f"Timeout exception occurred. Saving experiment_df and continuing...")
                    retry_count += 1
                    time.sleep(5)
            if not success:
                print("All retries failed. Saving experiment_df and continuing...")
                continue

            # Retrieve the text generated by ChatGPT and calculate its Lexile score.
            simp_text = response["choices"][0]["message"]["content"]
            simp_text = extract_question(simp_text)
            print(simp_text)

            sentences = re.split(r'[.!?]', simp_text)
            sentences = [sentence.strip() for sentence in sentences if sentence.strip()]
            if len(sentences)==0:
                print("****** len sen = 0 *********")
                continue
            else:
                simp_text_lexile_score = calculate_text_score(simp_text, "lexile")
            
            solvable = is_solvable(simp_text, answer)

            # Add the information to the experiment Datasets.
            experiment_sample_dict = {
                "Id": id,
                "Given Text": given_text,
                "G Lexile": G_lexile,
                "Answer": answer,
                "massage": messages,
                "Simplified Text": simp_text,
                "S Lexile": simp_text_lexile_score,
                "Solvable": solvable,
                "Iteration": iteration}
            
            experiment_df = pd.concat([experiment_df, pd.DataFrame([experiment_sample_dict])], ignore_index=True)
            
            messages.append({"role": "assistant", "content": simp_text})

            if prompt_detail == "base":
                messages.append({"role": "user","content": prompts_math.minimal_exp_res_prompt_base(solvable)})
            elif prompt_detail == "knowledge":
                syntax_lexile = calculate_text_score(simp_text, "syntax")
                lexical_lexile = calculate_text_score(simp_text, "lexical")
                if syntax_lexile > lexical_lexile :
                    highest_category = "syntax complexity"
                else:
                    highest_category = "lexical complexity"
                messages.append({"role": "user","content": prompts_math.minimal_exp_res_prompt_knowledge(solvable, simp_text_lexile_score, highest_category)})
            elif prompt_detail == "formula":
                syntax_lexile = calculate_text_score(simp_text, "syntax")
                lexical_lexile = calculate_text_score(simp_text, "lexical")
                decodability_lexile = calculate_text_score(simp_text, "decodability")
                messages.append({"role": "user","content": prompts_math.minimal_exp_res_prompt_formula(solvable, simp_text_lexile_score, syntax_lexile, lexical_lexile, decodability_lexile)})
            elif prompt_detail == "final":
                syntax_lexile = calculate_text_score(simp_text, "syntax")
                lexical_lexile = calculate_text_score(simp_text, "lexical")
                decodability_lexile = calculate_text_score(simp_text, "decodability")
                messages.append({"role": "user","content": prompts_math.minimal_exp_res_prompt_final(solvable, simp_text_lexile_score, syntax_lexile, lexical_lexile, decodability_lexile)})

            given_text = simp_text
            G_lexile = simp_text_lexile_score

    # Do something on Path
    output_file = os.path.abspath("experiment_results")
    output_file += f'/math/minimal_{prompt_detail}_experiment.csv'
    experiment_df.to_csv(output_file, index=False)

def target_lexile_score(dataset_name, sampels_num, iterations_num, prompt_detail,  target_lexile):
    experiment_df = pd.DataFrame(columns=["Id", "Given Text", "G Lexile","Answer","massage", "Simplified Text", "S Lexile","Solvable", "Iteration"])

    # upload the Datasets
    dataset = load_dataset(dataset_name, 'main')
    train_dataset = dataset["train"]

    # Run over "sampels_num" texts in the Datasets and try to simplify them using Gpt 3.5
    for text_number in range(3, 3+sampels_num):
        id = text_number
        given_text = train_dataset[text_number]["question"]
        answer = train_dataset[text_number]["answer"]

        G_lexile = calculate_text_score(given_text, "lexile")
        messages = prompts_math.target_exp_initial_prompt(prompt_detail, given_text, G_lexile, target_lexile)

        for iteration in range(1,1+iterations_num):
            retry_count = 0
            success = False
            while retry_count < 3:  # Retry up to 3 times
                try:
                    response = openai.ChatCompletion.create(
                        model=OPENAI_MODEL,
                        messages=messages,
                        max_tokens=160,
                    )
                    success = True
                    break
                except:
                    print(f"Timeout exception occurred. Saving experiment_df and continuing...")
                    retry_count += 1
                    time.sleep(5)
            if not success:
                print("All retries failed. Saving experiment_df and continuing...")
                continue

            # Retrieve the text generated by ChatGPT and calculate its Lexile score.
            simp_text = response["choices"][0]["message"]["content"]
            simp_text = extract_question(simp_text)
            print(simp_text)

            sentences = re.split(r'[.!?]', simp_text)
            sentences = [sentence.strip() for sentence in sentences if sentence.strip()]
            if len(sentences)==0:
                print("****** len sen = 0 *********")
                continue
            else:
                simp_text_lexile_score = calculate_text_score(simp_text, "lexile")

            solvable = is_solvable(simp_text, answer)

            # Add the information to the experiment Datasets.
            experiment_sample_dict = {
                "Id": id,
                "Given Text": given_text,
                "G Lexile": G_lexile,
                "Answer": answer,
                "massage": messages,
                "Simplified Text": simp_text,
                "S Lexile": simp_text_lexile_score,
                "Solvable": solvable,
                "Iteration": iteration}
            
            experiment_df = pd.concat([experiment_df, pd.DataFrame([experiment_sample_dict])], ignore_index=True)
            
            messages.append({"role": "assistant", "content": simp_text})

            if prompt_detail == "base":
                messages.append({"role": "user","content": prompts_math.target_exp_res_prompt_base(solvable, simp_text_lexile_score, target_lexile)})
            elif prompt_detail == "knowledge":
                syntax_lexile = calculate_text_score(simp_text, "syntax")
                lexical_lexile = calculate_text_score(simp_text, "lexical")
                messages.append({"role": "user","content": prompts_math.target_exp_res_prompt_knowledge(solvable, simp_text_lexile_score, target_lexile, syntax_lexile, lexical_lexile)})
            elif prompt_detail == "formula":
                syntax_lexile = calculate_text_score(simp_text, "syntax")
                lexical_lexile = calculate_text_score(simp_text, "lexical")
                decodability_lexile = calculate_text_score(simp_text, "decodability")
                messages.append({"role": "user","content": prompts_math.target_exp_res_prompt_formula(solvable, simp_text_lexile_score, syntax_lexile, lexical_lexile, decodability_lexile)})
            elif prompt_detail == "final":
                syntax_lexile = calculate_text_score(simp_text, "syntax")
                lexical_lexile = calculate_text_score(simp_text, "lexical")
                decodability_lexile = calculate_text_score(simp_text, "decodability")
                messages.append({"role": "user","content": prompts_math.target_exp_res_prompt_final(solvable, simp_text_lexile_score, syntax_lexile, lexical_lexile, decodability_lexile)})

            given_text = simp_text
            G_lexile = simp_text_lexile_score

    # Do something on Path
    output_file = os.path.abspath("experiment_results")
    output_file += f'/math/target_{prompt_detail}_experiment{target_lexile}.csv'
    experiment_df.to_csv(output_file, index=False)

def one_axis_lexile_score(dataset_name, sampels_num, iterations_num, prompt_detail, category):
    experiment_df = pd.DataFrame(columns=["Id", "Given Text", "G Lexile","Answer","massage", "Simplified Text", "S Lexile","Solvable", "Iteration"])

    # upload the Datasets
    dataset = load_dataset(dataset_name, 'main')
    train_dataset = dataset["train"]

    for text_number in range(3, 3+sampels_num):
        id = text_number
        given_text = train_dataset[text_number]["question"]
        answer = train_dataset[text_number]["answer"]

        if category == "syntax":
            G_category = calculate_text_score(given_text, "syntax")
        elif category == "lexical":
            G_category = calculate_text_score(given_text, "lexical")
        else:
            G_category = calculate_text_score(given_text, "decodability")
        G_syntax = calculate_text_score(given_text, "syntax")
        G_lexical = calculate_text_score(given_text, "lexical")
        G_decodability = calculate_text_score(given_text, "decodability")

        G_category = G_syntax if category == "syntax" else (G_lexical if category == "lexical" else G_decodability)

        messages = prompts_math.one_axis_initial_prompt(prompt_detail, given_text, category, G_category)

        for iteration in range(1,1+iterations_num):
            retry_count = 0
            success = False
            while retry_count < 3:  # Retry up to 3 times
                try:
                    response = openai.ChatCompletion.create(
                        model=OPENAI_MODEL,
                        messages=messages,
                        max_tokens=160,
                    )
                    success = True
                    break
                except:
                    print(f"Timeout exception occurred. Saving experiment_df and continuing...")
                    retry_count += 1
                    time.sleep(5)
            if not success:
                print("All retries failed. Saving experiment_df and continuing...")
                continue

            # Retrieve the text generated by ChatGPT and calculate its Lexile score.
            simp_text = response["choices"][0]["message"]["content"]
            simp_text = extract_question(simp_text)
            print(simp_text)

            sentences = re.split(r'[.!?]', simp_text)
            sentences = [sentence.strip() for sentence in sentences if sentence.strip()]
            if len(sentences)==0:
                print("****** len sen = 0 *********")
                continue
            else:
                simp_text_syntax_score = calculate_text_score(simp_text, "syntax")
                simp_text_lexical_score = calculate_text_score(simp_text, "lexical")
                simp_text_decodability_score = calculate_text_score(simp_text, "decodability")
                simp_text_category_score = simp_text_syntax_score if category == "syntax" else (simp_text_lexical_score if category == "lexical" else simp_text_decodability_score)

            solvable = is_solvable(simp_text, answer)

            # Add the information to the experiment Datasets.
            experiment_sample_dict = {
                "Id": id,
                "Given Text": given_text,
                "G syntax": G_syntax,
                "G lexical": G_lexical,
                "G decodability": G_decodability,
                "Answer": answer,
                "massage": messages,
                "Simplified Text": simp_text,
                "S syntax": simp_text_syntax_score,
                "S lexical": simp_text_lexical_score,
                "S decodability": simp_text_decodability_score,
                "Solvable": solvable,
                "Iteration": iteration}
            
            experiment_df = pd.concat([experiment_df, pd.DataFrame([experiment_sample_dict])], ignore_index=True)
            
            messages.append({"role": "assistant", "content": simp_text})

            if prompt_detail == "base":
                messages.append({"role": "user","content": prompts_math.one_axis_exp_res_prompt_base(solvable, simp_text_category_score, category)})
            elif prompt_detail == "knowledge":
                messages.append({"role": "user","content": prompts_math.one_axis_exp_res_prompt_knowledge(solvable, simp_text_category_score, category)})
            elif prompt_detail == "formula":
                continue
            elif prompt_detail == "final":
                continue
            
            given_text = simp_text
            G_syntax = simp_text_syntax_score
            G_lexical = simp_text_lexical_score
            G_decodability = simp_text_decodability_score

    # Do something on Path
    output_file = os.path.abspath("experiment_results")
    output_file += f'/math/target_{prompt_detail}_experiment{category}.csv'
    experiment_df.to_csv(output_file, index=False)