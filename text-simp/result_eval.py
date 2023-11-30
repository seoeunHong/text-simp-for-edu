import numpy as np
import pandas as pd

def minimal_lexile_score(exprerience_path):
    # run this for get the list of scores for the first experiment - minimal Lexile score
    # i put the mean of this list in the table
    df = pd.read_csv(exprerience_path)
    Lexile_lowest_list = []
    grouped = df.groupby('Id')
    for group_id, group_df in grouped:
        base_score = group_df['G Lexile'].iloc[0]
        solvable_rows = group_df[group_df['Solvable'] == True]
        if not solvable_rows.empty:
            # Calculate Lexile_lowest based on filtered rows
            Lexile_lowest_list.append(min(solvable_rows['S Lexile'].min(), base_score))
        else:
            # If there are no solvable rows, use the G Lexile value
            Lexile_lowest_list.append( base_score)
    print(f"Lexile_lowest_list: {Lexile_lowest_list}")
    return Lexile_lowest_list

def dis_from_target_calculation (row):
    return abs(row['S Lexile'] - TARGET_SCORE)

def dis_from_target(exprerience_path):
    # run this for get the list of scores for the second experiment - dis from target Lexile score
    # i put the mean of this list in the table
    df = pd.read_csv(exprerience_path)
    df['dis_from_target'] = df.apply(dis_from_target_calculation, axis=1)
    Lexile_dis_list = []
    grouped = df.groupby('Id')
    for group_id, group_df in grouped:
        base_dis = abs(group_df['G Lexile'].iloc[0] - TARGET_SCORE)
        solvable_rows = group_df[group_df['Solvable'] == True]
        if not solvable_rows.empty:
            # Calculate Lexile_lowest based on filtered rows
            Lexile_dis_list.append(min(solvable_rows['dis_from_target'].min(), base_dis))
        else:
            # If there are no solvable rows, use the G Lexile value
            Lexile_dis_list.append(base_dis)
    return Lexile_dis_list


def one_axis_score_lexical(exprerience_path):
    # run this for get the list of scores for the third experiment - move just on one axis
    # i put the mean of each of this list in the table. in this lexical experiment we want big lexical fiff and all the other small
    df = pd.read_csv(exprerience_path)
    lexical_simplified_by = []
    syntax_simplified_by = []
    decodability_simplified_by = []

    grouped = df.groupby('Id')

    for group_id, group_df in grouped:
        base_lexical_score = group_df["G lexical"].iloc[0]
        base_syntax_score =  group_df["G syntax"].iloc[0]
        base_decodability_score = group_df["G decodability"].iloc[0]

        solvable_rows = group_df[group_df['Solvable'] == True]
        if not solvable_rows.empty:
            # Calculate Lexile_lowest based on filtered rows
            min_score = solvable_rows["S lexical"].min()

            if min_score<base_lexical_score:
                min_score_info = solvable_rows[solvable_rows["S lexical"] == min_score]
                lexical_simplified_by.append(base_lexical_score - min_score)
                syntax_simplified_by.append(base_syntax_score- min_score_info["S syntax"].iloc[0])
                decodability_simplified_by.append(base_decodability_score - min_score_info["S decodability"].iloc[0])
            else:
                lexical_simplified_by.append(0)
                syntax_simplified_by.append(0)
                decodability_simplified_by.append(0)
        else:
            # If there are no solvable rows, use the G Lexile value
            lexical_simplified_by.append(0)
            syntax_simplified_by.append(0)
            decodability_simplified_by.append(0)
    return lexical_simplified_by, syntax_simplified_by, decodability_simplified_by


def one_axis_score_syntax(exprerience_path):
    # run this for get the list of scores for the third experiment - move just on one axis
    # i put the mean of each of this list in the table. in this lexical experiment we want big lexical fiff and all the other small
    df = pd.read_csv(exprerience_path)
    lexical_simplified_by = []
    syntax_simplified_by = []
    decodability_simplified_by = []

    grouped = df.groupby('Id')

    for group_id, group_df in grouped:
        base_lexical_score = group_df["G lexical"].iloc[0]
        base_syntax_score =  group_df["G syntax"].iloc[0]
        base_decodability_score = group_df["G decodability"].iloc[0]

        solvable_rows = group_df[group_df['Solvable'] == True]
        if not solvable_rows.empty:
            # Calculate syntax_lowest based on filtered rows
            min_score = solvable_rows["S syntax"].min()

            if min_score<base_syntax_score:
                min_score_info = solvable_rows[solvable_rows["S syntax"] == min_score]
                lexical_simplified_by.append(base_lexical_score - min_score_info["S lexical"].iloc[0])
                syntax_simplified_by.append(base_syntax_score- min_score)
                decodability_simplified_by.append(base_decodability_score - min_score_info["S decodability"].iloc[0])
            else:
                lexical_simplified_by.append(0)
                syntax_simplified_by.append(0)
                decodability_simplified_by.append(0)
        else:
            # If there are no solvable rows, use the G Lexile value
            lexical_simplified_by.append(0)
            syntax_simplified_by.append(0)
            decodability_simplified_by.append(0)
    return lexical_simplified_by, syntax_simplified_by, decodability_simplified_by

if __name__ == '__main__':
    # First experience
    '''
    print("*************************base*****************************")
    score_list = minimal_Lexile_score("Prompt_experiments/minimal_Base_experiment.csv")
    print("base's results:", score_list)
    print("means minimal Lexile score:", np.mean(score_list))
    
    print("************************* minimal_specific_knowledge_experiment *****************************")
    score_list = minimal_Lexile_score("Prompt_experiments/minimal_specific_knowledge_experiment.csv")
    print("minimal_specific_knowledge_experiment's results:", score_list)
    print("means minimal Lexile score:", np.mean(score_list))
 
    
    print("************************* target formula experiment *****************************")
    score_list = minimal_Lexile_score("Prompt_experiments/minimal_formula_experiment.csv")
    print("minimal_specific_knowledge_experiment's results:", score_list)
    print("means minimal Lexile score:", np.mean(score_list))
    '''
    '''
    print("************************* minimal_final_experiment *****************************")
    score_list = minimal_Lexile_score("Prompt_experiments/minimal_final_experiment.csv")
    print("minimal_final_experiment's results:", score_list)
    print("means minimal Lexile score:", np.mean(score_list))
    print("means dis Lexile score:", np.var(score_list))

    print("************************* target bast 1200 fixed experiment *****************************")
    score_list = dis_from_target("Prompt_experiments/target_final_1200_experiment.csv")
    print("target final 900 experiment experiment's results:", score_list)
    print("means minimal Lexile score:", np.mean(score_list))
    print("means dis Lexile score:", np.var(score_list))

    '''
    print("************************* target bast 700 fixed experiment *****************************")
    score_list = dis_from_target("Prompt_experiments/target_final_700_experiment.csv")
    print("target final 700 experiment experiment's results:", score_list)
    print("means dis Lexile score:", np.var(score_list))

    print("************************* target bast 1200 fixed experiment *****************************")
    score_list = dis_from_target("Prompt_experiments/target_final_1200_experiment.csv")
    print("target final 700 experiment experiment's results:", score_list)
    print("means dis Lexile score:", np.var(score_list))
    TARGET_SCORE = 900
    '''
    # second experimence
    print("************************* target base experiment *****************************")
    score_list = dis_from_target("Prompt_experiments/target_Base_experiment900.csv")
    print("target base experiment's results:", score_list)
    print("means dis Lexile score:", np.mean(score_list))

    print("************************* target knowledge experiment *****************************")
    score_list = dis_from_target("Prompt_experiments/target_knowledge_experiment900.csv")
    print("target knowledge experiment's results:", score_list)
    print("means dis Lexile score:", np.mean(score_list))

    print("************************* target formula experiment *****************************")
    score_list = dis_from_target("Prompt_experiments/target_formula_experiment1200.csv")
    print("target knowledge experiment's results:", score_list)
    print("means dis Lexile score:", np.mean(score_list))
    '''

    #third experimence

    #third experimence
    '''
        print("************************* one axis base experiment *****************************")
    score_list = one_axis_score_syntax("Prompt_experiments/one_axis_base_experiment_syntax.csv")
    print("one axis base experiment's syntax simplification list:", score_list[1])
    print("one axis base experiment's syntax simplification mean:", np.mean(score_list[1]))
    print("one axis base experiment's lexical simplification mean:", np.mean(score_list[0]))
    print("one axis base experiment's decodability simplification mean:", np.mean(score_list[2]))

    print("************************* one axis knowledge experiment *****************************")
    score_list = one_axis_score_syntax("Prompt_experiments/one_axis_knowledge_experiment_syntax.csv")
    print("one axis base experiment's syntax simplification list:", score_list[1])
    print("one axis base experiment's syntax simplification mean:", np.mean(score_list[1]))
    print("one axis base experiment's lexical simplification mean:", np.mean(score_list[0]))
    print("one axis base experiment's decodability simplification mean:", np.mean(score_list[2]))
    '''
    '''
       print("************************* one axis base experiment *****************************")
    score_list = one_axis_score_lexical("Prompt_experiments/one_axis_base_experiment_lexical.csv")
    print("one axis base experiment's lexical simplification list:", score_list[0])
    print("one axis base experiment's lexical simplification mean:", np.mean(score_list[0]))
    print("one axis base experiment's syntax simplification mean:", np.mean(score_list[1]))
    print("one axis base experiment's decodability simplification mean:", np.mean(score_list[2]))
    
    print("************************* one axis knowledge experiment *****************************")
    score_list = one_axis_score_lexical("Prompt_experiments/one_axis_knowledge_experiment_lexical.csv")
    print("one axis base experiment's lexical simplification list:", score_list[0])
    print("one axis base experiment's lexical simplification mean:", np.mean(score_list[0]))
    print("one axis base experiment's syntax simplification mean:", np.mean(score_list[1]))
    print("one axis base experiment's decodability simplification mean:", np.mean(score_list[2]))

    '''