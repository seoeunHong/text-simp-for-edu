UNSOLVABLE_PROMPT = f"The generated text appears to be unsolvable as it lacks the essential information needed to solve the problem. Please try again and ensure that the simplified text remains solvable. \n Return just the simplified text. The simplified text is:"

def minimal_detailed_prompt(given_text, cur_lexile_score):
    return f"As a text simplification expert specializing in mathematical questions, your goal is to enhance the text's readability by lowering Lexile score while ensuring it remains solvable with the same answer. \
        Consider that the Lexile score is calculated based on several features and their respective weights: \
        Average number of words in a sentence: 20.44 \
        Average number of characters in a sentence: 8.92 \
        Average parsing tree depth of a sentence: 69.34 \
        Maximum nesting level of the text: 0.89 \
        Average number of punctuations in a sentence: -38.28 \
        Average number of entities in a sentence: 17.98 \
        Average number of unique parts of speech in a sentence: 14.55 \
        Average number of words that appear in the DallChall list: -57.70 \
        Average number of syllables in a sentence: -4.92 \
        Average number of words with 3 or more syllables in a sentence: -7.73 \
        Average Kuperman Age of Acquisition (AoA) result of a sentence: 3.51 \
        Average Type-Token Ratio (TTR) score of a sentence: -59.11 \
        Average difference between the number of letters and phonemes in words: -25.43 \
        Average probability of grapheme-to-phoneme correspondences per word: 420.65 \
        These features can be categorized into three complexity factors: \
        Syntax complexity - determined by factors such as the number of words and characters, parsing tree depth, maximum nesting level, punctuation count, and the number of entity and POS tags. \
        Lexical complexity - assessed based on the number of words in the DallChall list, syllable count, the number of difficult words (according to syllables), and Kuperman Age of Acquisition (AoA). \
        Decodability complexity - calculated using metrics like type-token ratio (TTR), letter sound discrepancy, and average grapheme-phoneme correspondences (GPCs) probability. \
        Now, here's a math problem for you to simplify: {given_text}. \
        The problem's current Lexile score is: {cur_lexile_score}. \
        Please simplify the text while preserving its original meaning. \
        Return just the simplified text. The simplified text is:"

def minimal_exp_initial_prompt(prompt_detail, given_text, cur_lexile_score):
    messages = []
    prompt_detail = prompt_detail.lower()
    prompt = ""
    if prompt_detail == "base":
        prompt = f"As a text simplification agent specialized in math problems, your goal is to enhance the readability of mathematical questions while ensuring they remain solvable with the same answer. \
        Here's a math problem for you to simplify: {given_text}.\
        Please simplify the text while preserving its original meaning. \n The simplified text:"
    elif prompt_detail == "knowledge":
        prompt = f"As a text simplification agent specialized in math problems, your goal is to enhance the readability of mathematical questions while ensuring they remain solvable with the same answer. \
        Let's consider readability complexity, which is evaluated using a Lexile score. Lexile takes into account three main factors:\
        1. Syntax complexity - Determined by factors such as the number of words and characters, parsing tree depth, maximum nesting level, punctuation count, and the number of entity and POS tags.\
        2. Lexical complexity - Assessed based on the number of words in the DallChall list, syllables count, the number of difficult words (according to syllables), and Kuperman Age of Acquisition (AoA).\
        3. Decodability complexity - Calculated using metrics like type-token ratio (ttr), letter sound discrepancy, and average grapheme-phoneme correspondences (GPCs) probability.\
        Here's a math problem for you to simplify: {given_text}.\
        The problem's current Lexile score is: {cur_lexile_score}.\
        Please simplify the text while preserving its original meaning. \n The simplified text:"
    elif prompt_detail == "formula":
        prompt = minimal_detailed_prompt(given_text, cur_lexile_score)
    elif prompt_detail == "fewshots":
        first_q = "According to its nutritional info, a bag of chips has 250 calories per serving. If a 300g bag has 5 servings, how many grams can you eat if your daily calorie target is 2000 and you have already consumed 1800 calories?"
        first_lexile = 1205.4693835487653
        second_q = "Grandma Jones baked 5 apple pies for the fireman's luncheon. She cut each pie into 8 even pieces and set the five pies out on the buffet table for the guests to serve themselves. At the end of the evening, after the guests had taken and eaten their pieces of pie, there were 14 pieces of pie remaining. How many pieces were taken by the guests durring the luncheon?"
        second_lexile = 891.9508634763805
        fewshot_examples = [
            first_q,
            first_lexile,
            minimal_detailed_prompt(first_q, first_lexile),
            "Looking at the nutrition facts, a 300g bag of chips has 5 servings, each with 250 calories. If you've already had 1800 calories today and your daily goal is 2000, how many grams of chips can you still enjoy?",
            "Your simplified problem Lexile Score is: 1098.4092581023986 \n Currently syntax complexity is 1009.3940529883826 ,lexical complexity is 1097.3881933087077 and decodability complexity is 688.8043087823326. \n Please continue to simplify the problem to achieve the lowest Lexile score while preserving its original meaning. \n Return just the simplified problem. The simplified problem is:",
            "A bag of chips has 250 calories per serving. The bag weighs 300g and has 5 servings. If you've eaten 1800 calories today and aim for 2000, how many more grams of chips can you eat?"
            "Your simplified problem Lexile Score is: 772.4218123086275 \n Currently syntax complexity is 661.4118508957401 ,lexical complexity is 740.9048603256444 and decodability complexity is 684.7118038726977. \n Please continue to simplify the problem to achieve the lowest Lexile score while preserving its original meaning. \n Return just the simplified problem. The simplified problem is:",
            "A bag of chips weighs 300g and has 5 servings. Each serving contains 250 calories. If you've had 1800 calories and want to reach 2000, how many more grams of chips can you eat?",
            second_q,
            second_lexile,
            minimal_detailed_prompt(second_q, second_lexile),
            "Grandma Jones baked 5 pies for the fireman's lunch. She sliced each pie into 8 pieces and placed them on the buffet table. At the end of the evening, after the guests had taken and eaten their pieces of pie, there were 14 pieces of pie left. How many pieces  did the guests take?",
            "Your simplified problem Lexile Score is: 785.1043056236798 \n Currently syntax complexity is 814.0333553177685 ,lexical complexity is 789.8478011640233 and decodability complexity is 731.2254497465956. \n Please continue to simplify the problem to achieve the lowest Lexile score while preserving its original meaning. \n Return just the simplified problem. The simplified problem is:",
            "Grandma Jones made 5 pies, each with 8 pieces, for the fireman's luncheon. The guests served themselves from the buffet table. After everyone ate, 14 pieces of pie were left. How many pieces did the guests take?",
            "Your simplified problem Lexile Score is: 698.9623714625961 \n Currently syntax complexity is 671.6400816232775 ,lexical complexity is 681.6386811785961 and decodability complexity is 773.4679290103579. \n Please continue to simplify the problem to achieve the lowest Lexile score while preserving its original meaning. \n Return just the simplified problem. The simplified problem is:",
            "Grandma Jones baked 5 pies for the fireman's lunch, each with 8 pieces. After the guests ate, 14 pieces were left. How many pieces did the guests take?"
        ]

        n = len(fewshot_examples)
        for i in range(n):
            if i % 2 == 0:
                messages.append({"role": "user", "content": fewshot_examples[i]})
            else:
                messages.append({"role": "assistant", "content": fewshot_examples[i]})
        prompt = minimal_detailed_prompt(given_text, cur_lexile_score)
    messages.append({"role": "user", "content": prompt})
    return messages

def minimal_exp_res_prompt_base(solvable):
    prompt = ""
    if solvable:
        prompt = "Please continue to simplify the text further while preserving its original meaning. \n The simplified text:"
    else:
        prompt = "The generated text appears to be unsolvable as it lacks the essential information needed to solve the problem. Please try again and ensure that the simplified text remains solvable. \n Return just the simplified text. The simplified text is:"
    return prompt

def minimal_exp_res_prompt_knowledge(solvable, simp_text_lexile_score, highest_category):
    prompt = ""
    if solvable:
        prompt = f"Your generated text Lexile score is {simp_text_lexile_score}, Please continue to simplify the text further while preserving its original meaning. Try to focus on simplify the text's {highest_category}.\n The simplified text:"
    else:
        prompt = "The generated text appears to be unsolvable as it lacks the essential information needed to solve the problem. Please try again and ensure that the simplified text remains solvable. \n Return just the simplified text. The simplified text is:"
    return prompt

def minimal_exp_res_prompt_formula(solvable, simp_text_lexile_score, syntax_lexile, lexical_lexile, decodability_lexile):
    prompt = ""
    if solvable:
        prompt = f"Your generated text Lexile Score is: {simp_text_lexile_score}\n Currently syntax complexity is {syntax_lexile} ,lexical complexity is {lexical_lexile} and decodability complexity is {decodability_lexile}. \n Please continue to simplify the text further while preserving its original meaning. \n Return just the simplified text. The simplified text is:"
    else:
        prompt = "The generated text appears to be unsolvable as it lacks the essential information needed to solve the problem. Please try again and ensure that the simplified text remains solvable. \n Return just the simplified text. The simplified text is:"
    return prompt

def minimal_exp_res_prompt_final(solvable, simp_text_lexile_score, syntax_lexile, lexical_lexile, decodability_lexile):
    prompt = ""
    if solvable:
        prompt = f"Your simplified problem Lexile Score is: {simp_text_lexile_score}\n Currently syntax complexity is {syntax_lexile} ,lexical complexity is {lexical_lexile} and decodability complexity is {decodability_lexile}. \n Please continue to simplify the problem to achieve the lowest Lexile score while preserving its original meaning. \n Return just the simplified problem. The simplified problem is:"
    else:
        prompt = "The generated text appears to be unsolvable as it lacks the essential information needed to solve the problem. Please try again and ensure that the simplified text remains solvable. \n Return just the simplified text. The simplified text is:"
    return prompt

def target_detail_prompt(given_text, cur_lexile_score, target_lexile):
    return f"As a text readability expert specializing in mathematical problems, your goal is to rephrase the problem so its readability level will match a given target Lexile score while ensuring the problem remains solvable with the same answer.\
           Consider that the Lexile score is calculated based on several features and their respective weights: \
           Average number of words in a sentence: 20.44 \
           Average number of characters in a sentence: 8.92 \
           Level of complexity in understanding how the words in a sentence are interconnected  : 69.34 \
           Average number of punctuations in a sentence: -38.28 \
           Average number of entities in a sentence: 17.98 \
           Average number of unique parts of speech in a sentence: 14.55 \
           Average number of common words: -57.70 \
           Average number of syllables in a sentence: -4.92 \
           Average number of words with 3 or more syllables in a sentence: -7.73 \
           Average Age of Acquisition of the words in a sentence: 3.51 \
           The diversity of words in a text by comparing the number of unique words to the total number of words: -59.11 \
           Average difference between the number of letters and phonemes in words: -25.43 \
           How rare the combination of grapheme-phoneme correspondences per word: 420.65 \
           These features can be categorized into three complexity factors: \
           Syntax complexity - determined by factors such as the number of words and characters, parsing tree depth, maximum nesting level, punctuation count, and the number of entity and POS tags. \
           Lexical complexity - assessed based on the number of words in the DallChall list, syllable count, the number of difficult words (according to syllables), and Kuperman Age of Acquisition (AoA). \
           Decodability complexity - calculated using metrics like type-token ratio (TTR), letter sound discrepancy, and average grapheme-phoneme correspondences (GPCs) probability. \
           Now, here's a math problem for you to rephrase: {given_text}. \
           The problem's current Lexile score is: {cur_lexile_score}. \
           The target Lexile score for this problem is: {target_lexile}. \
           Please rephrase the problem to achieve the target Lexile score while preserving its original meaning. \
           Return just the rephrased problem. The rephrased problem is:"

def generate_fewshot_examples(target_lexile):
    fewshot_examples = []
    if target_lexile == 700:
        first_q = "According to its nutritional info, a bag of chips has 250 calories per serving. If a 300g bag has 5 servings, how many grams can you eat if your daily calorie target is 2000 and you have already consumed 1800 calories?"
        first_lexile = 1205.4693835487653
        second_q = "In a dance class of 20 students, 20% enrolled in contemporary dance, 25% of the remaining enrolled in jazz dance, and the rest enrolled in hip-hop dance. What percentage of the entire students enrolled in hip-hop dance?"
        second_lexile = 1182.7259064906186

        fewshot_examples = [
            first_q,
            first_lexile,
            target_detail_prompt(first_q, first_lexile, 700),
            "Looking at the nutrition facts, a 300g bag of chips has 5 servings, each with 250 calories. If you've already had 1800 calories today and your daily goal is 2000, how many grams of chips can you still enjoy?",
            "Your rephrased problem Lexile Score is: 1098.4092581023986 \n Target Lexile Score is: 700. \n Currently syntax complexity is 1009.3940529883826 ,lexical complexity is 1097.3881933087077 and decodability complexity is 688.8043087823326. \n Please continue to rephrase the problem to achieve the target Lexile score of 700 while preserving its original meaning. \n Return just the rephrased problem. The rephrased problem is:",
            "A bag of chips that weighs 300g has 5 servings. Each serving containing 250 calories. If you've already consumed 1800 calories today and aim for 2000, how many more grams of chips can you enjoy?",
            "Your rephrased problem Lexile Score is: 879.2910290240773 \n Target Lexile Score is: 700. \n Currently syntax complexity is 825.9428138893685 ,lexical complexity is 812.1659042966221 and decodability complexity is 730.4002966209815. \n Please continue to rephrase the problem to achieve the target Lexile score of 700 while preserving its original meaning. \n Return just the rephrased problem. The rephrased problem is:",
            "A bag of chips has 250 calories per serving. The bag weighs 300g and has 5 servings. If you've eaten 1800 calories today and aim for 2000, how many more grams of chips can you eat?",
            second_q,
            second_lexile,
            target_detail_prompt(second_q, second_lexile, 700),
            "In a dance class with 20 students, 20% chose contemporary dance. Then, 25% of the rest picked jazz dance, and the rest chose hip-hop dance. What's the percentage of students in hip-hop dance?",
            "Your generated text Lexile Score is: 955.2236214716519\n Target Lexile Score is: 700. \n Currently syntax complexity is 866.467620228928 ,lexical complexity is 810.2116428663053 and decodability complexity is 815.3307423746944. \n Please continue to rephrase the text to achieve the target Lexile score of 700 while preserving its original meaning. \n Return just the rephrased text. The rephrased text is:",
            "Out of 20 students, 20% chose contemporary dance. 25% of the rest chose jazz. The rest went for hip-hop. What's the percentage of students in hip-hop dance?",
            "Your generated text Lexile Score is: 705.6859538262045\n Target Lexile Score is: 700. \n Currently syntax complexity is  660.6654156774044 ,lexical complexity is 603.6819907644496 and decodability complexity is 937.2790346840508. \n Please continue to rephrase the text to achieve the target Lexile score of 700 while preserving its original meaning. \n Return just the rephrased text. The rephrased text is:",
            "Among 20 students, 20% picked contemporary dance. Then, 25% of the others selected jazz. The remaining students chose hip-hop. What's the percentage in the hip-hop dance group?"
        ]
    elif target_lexile == 900:
        first_p = "According to its nutritional info, a bag of chips has 250 calories per serving. If a 300g bag has 5 servings, how many grams can you eat if your daily calorie target is 2000 and you have already consumed 1800 calories?"
        first_lexile = 1205.4693835487653
        second_q = "In a dance class of 20 students, 20% enrolled in contemporary dance, 25% of the remaining enrolled in jazz dance, and the rest enrolled in hip-hop dance. What percentage of the entire students enrolled in hip-hop dance?"
        second_lexile = 1182.7259064906186

        fewshot_examples = [
            first_p,
            first_lexile,
            target_detail_prompt(first_q, first_lexile, 900),
            "Looking at the nutrition facts, a 300g bag of chips has 5 servings, each with 250 calories. If you've already had 1800 calories today and your daily goal is 2000, how many grams of chips can you still enjoy?",
            "Your rephrased problem Lexile Score is: 1098.4092581023986 \n Target Lexile Score is: 900. \n Currently syntax complexity is 1009.3940529883826 ,lexical complexity is 1097.3881933087077 and decodability complexity is 688.8043087823326. \n Please continue to rephrase the problem to achieve the target Lexile score of 900 while preserving its original meaning. \n Return just the rephrased problem. The rephrased problem is:",
            "A bag of chips that weighs 300g has 5 servings. Each serving containing 250 calories. If you've already consumed 1800 calories today and aim for 2000, how many more grams of chips can you enjoy?",
            "Your rephrased problem Lexile Score is: 879.2910290240773 \n Target Lexile Score is: 900. \n Currently syntax complexity is 825.9428138893685 ,lexical complexity is 812.1659042966221 and decodability complexity is 730.4002966209815. \n Please continue to rephrase the problem to achieve the target Lexile score of 900 while preserving its original meaning. \n Return just the rephrased problem. The rephrased problem is:",
            "One bag of chips weighs 300g and has 5 servings, with each serving containing 250 calories. Your goal is to consume 2000 calories, and you've already had 1800 calories. How many additional grams of chips can you eat?",
            second_q,
            second_lexile,
            target_detail_prompt(second_q, second_lexile, 900),
            "Out of 20 students, 20% chose contemporary dance. 25% of the rest chose jazz. The rest went for hip-hop. What's the percentage of students in hip-hop dance?"
            "Your generated text Lexile Score is: 705.6859538262045\n Target Lexile Score is: 900. \n Currently syntax complexity is  660.6654156774044 ,lexical complexity is 603.6819907644496 and decodability complexity is 937.2790346840508. \n Please continue to rephrase the text to achieve the target Lexile score of 900 while preserving its original meaning. \n Return just the rephrased text. The rephrased text is:"
            "In a dance class with 20 students, 20% chose contemporary dance. Then, 25% of the rest picked jazz dance, and the rest chose hip-hop dance. What's the percentage of students in hip-hop dance?"
            "Your generated text Lexile Score is: 955.2236214716519\n Target Lexile Score is: 900. \n Currently syntax complexity is 866.467620228928 ,lexical complexity is 810.2116428663053 and decodability complexity is 815.3307423746944. \n Please continue to rephrase the text to achieve the target Lexile score of 900 while preserving its original meaning. \n Return just the rephrased text. The rephrased text is:"
            "Among 20 students, 20% picked contemporary dance. Then, 25% of the others selected jazz. The remaining students chose hip-hop. What's the percentage in the hip-hop dance group?"
        ]
    elif target_lexile == 1200:
        first_p = "Hector purchased a container of gumballs. He gave 4 to Todd.  He gave twice as many as he had given Todd to Alisha, and then he gave 5 less than four times as many to Bobby as he had given to Alisha. If Hector had 6 gumballs remaining, what is the total number of gumballs that Hector purchased?."
        first_lexile = 808.1502422992719
        second_p = "When Freda cooks canned tomatoes into sauce, they lose half their volume. Each 16 ounce can of tomatoes that she uses contains three tomatoes. Freda’s last batch of tomato sauce made 32 ounces of sauce. How many tomatoes did Freda use?"
        second_lexile = 754.291386229277

        fewshot_examples = [
            first_p,
            first_lexile,
            target_detail_prompt(first_q, first_lexile, 1200),
            "Hector recently purchased a container filled with colorful gumballs. To start, he shared four of them with his friend, Todd. Following this, he gave Alisha twice as many gumballs as he gave Todd. Later, he provided Bobby with a quantity that was 5 less than four times the number he shared with Alisha. After these actions, Hector found himself with only 6 gumballs left. Can you figure out the total number of gumballs he initially bought?",
            "Your rephrased problem Lexile Score is: 880.8133368291806 \n Target Lexile Score is: 1200. \n Currently syntax complexity is 853.5127924116758 ,lexical complexity is 862.4122735782781 and decodability complexity is 930.7086103233053. \n Please continue to rephrase the problem to achieve the target Lexile score of 1200 while preserving its original meaning. \n Return just the rephrased problem. The rephrased problem is:",
            "Hector made a purchase of a container filled with colorful gumballs. Initially, he shared 4 of them with Todd. Following that, he distributed twice as many gumballs to Alisha as he did to Todd. Subsequently, he gave Bobby a quantity that was 5 fewer than four times the number he shared with Alisha. If Hector found himself with only 6 gumballs remaining, can you deduce the total number of gumballs he originally acquired?",
            "Your rephrased problem Lexile Score is: 1016.3033412865236 \n Target Lexile Score is: 1200. \n Currently syntax complexity is 968.3205435543937 ,lexical complexity is 1021.2015459883315 and decodability complexity is 813.5532398828104. \n Please continue to rephrase the problem to achieve the target Lexile score of 1200 while preserving its original meaning. \n Return just the rephrased problem. The rephrased problem is:",
            "Hector made a purchase of a container filled with colorful gumballs. His first move was to divide four of these gumballs with his friend, Todd. Subsequently, he allocated a quantity to Alisha, which was twice the number he shared with Todd and finally, he gave Bobby a quantity that fell short by 5 compared to four times the number he shared with Alisha. After these transactions, Hector found himself with six gumballs. Can you deduce the original total quantity of gumballs that Hector procured?",
            second_p,
            second_lexile,
            target_detail_prompt(second_q, second_lexile, 1200),
            "When Freda transforms canned tomatoes into sauce, they undergo a transformation in volume, losing half of their original size. Each 16-ounce can of tomatoes she employs contains three tomatoes. In her most recent batch of tomato sauce, she yielded 32 ounces of sauce. How many tomatoes did Freda utilize in this culinary endeavor?",
            "Your generated text Lexile Score is: 1051.205\n Target Lexile Score is: 1200. \n Currently syntax complexity is 971.7034524017012 ,lexical complexity is 1066.4380385908903 and decodability complexity is 929.9504038582693. \n Please continue to rephrase the text to achieve the target Lexile score of 1200 while preserving its original meaning. \n Return just the rephrased text. The rephrased text is:",
            "As Freda transforms canned tomatoes into sauce, they experience a significant volume reduction, dwindling to just half their original size. Each 16-ounce can of tomatoes she utilizes contains three tomatoes. In her most recent endeavor to create tomato sauce, she managed to produce 32 ounces of sauce. Can you determine the exact number of tomatoes Freda employed in this intricate culinary process?",
            "Your generated text Lexile Score is: 1277.5704935321155\n Target Lexile Score is: 1200. \n Currently syntax complexity is  1148.923634715697 ,lexical complexity is 1292.0056271634985 and decodability complexity is 913.9105725623202. \n Please continue to rephrase the text to achieve the target Lexile score of 1200 while preserving its original meaning. \n Return just the rephrased text. The rephrased text is:",
            "As Freda turns canned tomatoes into sauce, they experience a significant volume reduction, shrinking to just half their original size. Each 16-ounce can of tomatoes she has three tomatoes. In her most recent endeavor to create tomato sauce, she managed to produce 32 ounces of sauce. Can you determine the exact number of tomatoes Freda employed in this intricate culinary process?"
        ]
    else:
        print("We don't have examples for that lexile score.")
    return fewshot_examples

def target_exp_initial_prompt(prompt_detail, given_text, cur_lexile_score, target_lexile):
    messages = []
    prompt_detail = prompt_detail.lower()
    prompt = ""
    if prompt_detail == "base":
        prompt = f"As a text readability expert specializing in mathematical questions, your goal is to adjust the text's readability to match the target Lexile score while ensuring it remains solvable with the same answer. \
        Here's a math problem for you to adjust: {given_text}.\
        The target Lexile score for this problem is: {target_lexile}.\
        Please rephrase the text to achieve the target Lexile score while preserving its original meaning.\n The rephrased text:"
    elif prompt_detail == "knowledge":
        prompt = f"As a text readability expert specializing in mathematical questions, your goal is to adjust the text's readability to match the target Lexile score while ensuring it remains solvable with the same answer. \
        Consider that Lexile takes into account three main factors:\
        1. Syntax complexity - Determined by factors such as the number of words and characters, parsing tree depth, maximum nesting level, punctuation count, and the number of entity and POS tags.\
        2. Lexical complexity - Assessed based on the number of words in the DallChall list, syllables count, the number of difficult words (according to syllables), and Kuperman Age of Acquisition (AoA).\
        3. Decodability complexity - Calculated using metrics like type-token ratio (ttr), letter sound discrepancy, and average grapheme-phoneme correspondences (GPCs) probability.\
        Here's a math problem for you to adjust: {given_text}.\
        The problem's current Lexile score is: {cur_lexile_score}.\
        The target Lexile score for this problem is: {target_lexile}.\
        Please rephrase the text to achieve the target Lexile score while preserving its original meaning.\n The rephrased text:"
    elif prompt_detail == "formula":
        prompt = target_detail_prompt(given_text, cur_lexile_score, target_lexile)
    elif prompt_detail == "fewshots":
        fewshot_examples = generate_fewshot_examples(target_lexile)
        n = len(fewshot_examples)
        for i in range(n):
            if i % 2 == 0:
                messages.append({"role": "user", "content": fewshot_examples[i]})
            else:
                messages.append({"role": "assistant", "content": fewshot_examples[i]})
        prompt = minimal_detailed_prompt(given_text, cur_lexile_score)
    messages.append({"role": "user", "content": prompt})
    return messages

def target_exp_res_prompt_base(solvable, simp_text_lexile_score, target_lexile):
    prompt = ""
    if solvable:
        prompt = f"Your generated text Lexile Score is: {simp_text_lexile_score}\n Target Lexile Score is: {target_lexile}\n. Please continue to rephrase the text to achieve the target Lexile score while preserving its original meaning.\n The rephrased text:"
    else:
        prompt = "The generated text appears to be unsolvable as it lacks the essential information needed to solve the problem. Please try again and ensure that the rephrased text remains solvable. \n The rephrased text:"
    return prompt

def target_exp_res_prompt_knowledge(solvable, simp_text_lexile_score, target_lexile, syntax_lexile, lexical_lexile):
    prompt = ""
    if solvable:
        prompt = f"Your generated text Lexile Score is: {simp_text_lexile_score}\n Target Lexile Score is: {target_lexile}. \n Currently syntax complexity is {syntax_lexile} and lexical complexity is {lexical_lexile}. \n Please continue to rephrase the text to achieve the target Lexile score while preserving its original meaning. \n The rephrased text:"
    else:
        prompt = "The generated text appears to be unsolvable as it lacks the essential information needed to solve the problem. Please try again and ensure that the rephrased text remains solvable. \n The rephrased text:"
    return prompt

def target_exp_res_prompt_formula(solvable, simp_text_lexile_score, target_lexile, syntax_lexile, lexical_lexile, decodability_lexile):
    prompt = ""
    if solvable:
        prompt = f"Your generated text Lexile Score is: {simp_text_lexile_score}\n Target Lexile Score is: {target_lexile}. \n Currently syntax complexity is {syntax_lexile} ,lexical complexity is {lexical_lexile} and decodability complexity is {decodability_lexile}. \n Please continue to rephrase the text to achieve the target Lexile score of {target_lexile} while preserving its original meaning. \n Return just the rephrased text. The rephrased text is:"
    else:
        prompt = "The generated text appears to be unsolvable as it lacks the essential information needed to solve the problem. Please try again and ensure that the rephrased text remains solvable. \n Return just the rephrased text. The rephrased text is:"
    return prompt

def target_exp_res_prompt_final(solvable, simp_text_lexile_score, syntax_lexile, lexical_lexile, decodability_lexile):
    prompt = ""
    if solvable:
        prompt = f"Your simplified problem Lexile Score is: {simp_text_lexile_score}\n Currently syntax complexity is {syntax_lexile} ,lexical complexity is {lexical_lexile} and decodability complexity is {decodability_lexile}. \n Please continue to simplify the problem to achieve the lowest Lexile score while preserving its original meaning. \n Return just the simplified problem. The simplified problem is:"
    else:
        prompt = "The generated text appears to be unsolvable as it lacks the essential information needed to solve the problem. Please try again and ensure that the simplified text remains solvable. \n Return just the simplified text. The simplified text is:"
    return prompt

def category_exp(category):
    prompt = ""
    if category == "syntax":
        prompt = "Syntax complexity - Determined by factors such as the avg number of words and characters in sentence, the avg parsing tree depth, the avg maximum nesting level, the avg punctuation count, and the avg number of entity and POS tags."
    elif category == "lexical":
        prompt = "Lexical complexity - Assessed based on the avg number of words in the DallChall list,abg syllables count,avg number of difficult words (according to syllables), and avg Kuperman Age of Acquisition (AoA) score."
    else:
        prompt = "Decodability complexity - Calculated using metrics like type-token ratio (ttr), letter sound discrepancy, and average grapheme-phoneme correspondences (GPCs) probability."
    return prompt


def one_axis_initial_prompt(prompt_detail, given_text, category, G_category):
    messages = []
    prompt_detail = prompt_detail.lower()
    prompt = ""
    if prompt_detail == "base":
        prompt = f"As a text simplification agent specialized in math problems, your goal is to enhance the readability of mathematical questions while ensuring they remain solvable with the same answer. \
               Let's focus on {category} complexity for this task. \
               Here's a math problem for you to simplify: {given_text}.\
               Please simplify the text while preserving its original meaning with a focus on reducing {category} complexity. \n The simplified text:"
    elif prompt_detail == "knowledge":
        G_category_exp = category_exp(category)
        prompt = f"As a text simplification agent specialized in math problems, your goal is to enhance the readability of mathematical questions while ensuring they remain solvable with the same answer. \
               Let's focus on {category} complexity for this task. \
               {G_category_exp} \
               Here's a math problem for you to simplify: {given_text}.\
               The {category} complexity score of this text is: {G_category}.\
               Please simplify the text while preserving its original meaning with a focus on reducing {category} complexity. \n The simplified text:"
    '''
    elif prompt_detail == "formula":
        prompt = target_detail_prompt(given_text, cur_lexile_score, target_lexile)
    elif prompt_detail == "fewshots":
        fewshot_examples = generate_fewshot_examples(target_lexile)
        n = len(fewshot_examples)
        for i in range(n):
            if i % 2 == 0:
                messages.append({"role": "user", "content": fewshot_examples[i]})
            else:
                messages.append({"role": "assistant", "content": fewshot_examples[i]})
        prompt = minimal_detailed_prompt(given_text, cur_lexile_score)
    '''
    messages.append({"role": "user", "content": prompt})
    return messages

def one_axis_exp_res_prompt_base(solvable, simp_text_category_score, category):
    prompt = ""
    if solvable:
        prompt = f"Your generated text {category} complexity score is: {simp_text_category_score} \n  Please continue to simplify the text further while preserving its original meaning. Try to focus on simplify the text's {category}. \n The simplified text:"
    else:
        prompt =f"The generated text appears to be unsolvable as it lacks the essential information needed to solve the problem. Please try again and ensure that the rephrased text remains solvable. \n The simplified text:"
    return prompt

def one_axis_exp_res_prompt_knowledge(solvable, simp_text_category_score, category):
    prompt = ""
    G_category_exp = category_exp(category)
    if solvable:
        prompt = f"Your generated text {category} complexity score is: {simp_text_category_score} \n  Please continue to simplify the text further while preserving its original meaning. Try to focus on simplify the text's {category}. \n As remembered, {G_category_exp}\n The simplified text:"
    else:
        prompt = f"The generated text appears to be unsolvable as it lacks the essential information needed to solve the problem. Please try again and ensure that the rephrased text remains solvable. \n The simplified text:"
    return prompt