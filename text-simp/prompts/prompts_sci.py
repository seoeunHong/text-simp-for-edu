UNSOLVABLE_PROMPT = f"The generated text appears to be unsolvable as it lacks the essential information needed to solve the problem. Please try again and ensure that the simplified text remains solvable. \n Return just the simplified text. The simplified text is:"

def minimal_detailed_prompt(given_text, cur_lexile_score):
    return f"As a text simplification expert specializing in science questions, your goal is to enhance the text's readability by lowering Lexile score while ensuring it remains solvable with the same answer. \
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
        Now, here's a science problem for you to simplify: {given_text}. \
        The problem's current Lexile score is: {cur_lexile_score}. \
        Please simplify the text while preserving its original meaning. \
        Return just the simplified text. The simplified text is:"

def minimal_exp_initial_prompt(prompt_detail, given_text, cur_lexile_score):
    messages = []
    prompt_detail = prompt_detail.lower()
    prompt = ""
    if prompt_detail == "base":
        prompt = f"As a text simplification agent specialized in science problems, your goal is to enhance the readability of science questions while ensuring they remain solvable with the same answer. \
        Here's a science problem for you to simplify: {given_text}.\
        Please simplify the text while preserving its original meaning. \n The simplified text:"
    elif prompt_detail == "knowledge":
        prompt = f"As a text simplification agent specialized in science problems, your goal is to enhance the readability of science questions while ensuring they remain solvable with the same answer. \
        Let's consider readability complexity, which is evaluated using a Lexile score. Lexile takes into account three main factors:\
        1. Syntax complexity - Determined by factors such as the number of words and characters, parsing tree depth, maximum nesting level, punctuation count, and the number of entity and POS tags.\
        2. Lexical complexity - Assessed based on the number of words in the DallChall list, syllables count, the number of difficult words (according to syllables), and Kuperman Age of Acquisition (AoA).\
        3. Decodability complexity - Calculated using metrics like type-token ratio (ttr), letter sound discrepancy, and average grapheme-phoneme correspondences (GPCs) probability.\
        Here's a science problem for you to simplify: {given_text}.\
        The problem's current Lexile score is: {cur_lexile_score}.\
        Please simplify the text while preserving its original meaning. \n The simplified text:"
    elif prompt_detail == "formula":
        prompt = minimal_detailed_prompt(given_text, cur_lexile_score)
    elif prompt_detail == "fewshots":
        first_q = "The marsh willow herb is a plant native to the northeastern United States. It grows best in damp habitats. Which of the following environmental changes would most likely cause a decrease in the marsh willow herb population in an area? (A) a rainstorm lasting several weeks (B) a drought lasting twelve months (C) unusually low temperatures during the month of July (D) unusually high temperatures during the month of January"
        first_lexile = 1184.59208979144
        second_q = "Students want to plant a lemon tree at their school, but the cold winter temperatures in Massachusetts would kill the tree. Which of the following is the best solution to this problem? (A) planting several lemon trees together in a row (B) building a greenhouse to shelter the lemon tree (C) giving the lemon tree extra fertilizer in the winter (D) tying a stake to the lemon tree for support during the winter"
        second_lexile = 1058.90020342678
        fewshot_examples = [
            first_q,
            first_lexile,
            minimal_detailed_prompt(first_q, first_lexile),
            "The marsh willow herb is a plant native to the northeastern United States that thrives in damp environments. Which of the following environmental changes would most likely cause a decrease in the marsh willow herb population? (A) A rainstorm lasting several weeks (B) A drought lasting twelve months (C) Unusually low temperatures in July (D) Unusually high temperatures in January.",
            "Your simplified problem Lexile Score is: 1271.463611217292\n Currently syntax complexity is 1388.3572942909796 ,lexical complexity is 1293.832233159702 and decodability complexity is 646.3995769630423. \n Please continue to simplify the problem to achieve the lowest Lexile score while preserving its original meaning. \n Return just the simplified problem. The simplified problem is:",
            "Which environmental change is most likely to decrease the population of marsh willow herb in an area? (A) Rainstorm lasting weeks (B) Year-long drought (C) Unusually low July temperatures (D) Unusually high January temperatures.",
            "Your simplified problem Lexile Score is: 1166.5721665890585\n Currently syntax complexity is 1139.2832926886686 ,lexical complexity is 1284.8185748959793 and decodability complexity is 745.1726535145164. \n Please continue to simplify the problem to achieve the lowest Lexile score while preserving its original meaning. \n Return just the simplified problem. The simplified problem is:",
            "Which environmental change would decrease the marsh willow herb population? (A) Rainstorm lasting weeks (B) Year-long drought (C) Unusually low temperatures in July (D) Unusually high temperatures in January.",
            second_q,
            second_lexile,
            minimal_detailed_prompt(second_q, second_lexile),
            "Students want to plant a lemon tree at school, but the cold winter temperatures in Massachusetts would harm the tree. What is the best solution to this problem? (A) planting several lemon trees in a row (B) building a greenhouse for the lemon tree (C) giving extra fertilizer to the lemon tree in the winter (D) using a stake to support the lemon tree during the winter.",
            "Your simplified problem Lexile Score is: 970.6352512616515\n Currently syntax complexity is 1008.2000773349066 ,lexical complexity is 1214.2583122209785 and decodability complexity is 722.6761603609035. \n Please continue to simplify the problem to achieve the lowest Lexile score while preserving its original meaning. \n Return just the simplified problem. The simplified problem is:",
            "Students want to plant a lemon tree at their school, but the cold winter temperatures in Massachusetts would kill the tree. Which of the following solutions is best? (A) planting lemon trees together in a row (B) building a greenhouse for the lemon tree (C) giving the lemon tree extra fertilizer in winter (D) using a stake to support the lemon tree during winter.",
            "Your simplified problem Lexile Score is: 974.4602306802203\n Currently syntax complexity is 1012.1851966284703 ,lexical complexity is 1208.9312407626926 and decodability complexity is 717.3988145512805. \n Please continue to simplify the problem to achieve the lowest Lexile score while preserving its original meaning. \n Return just the simplified problem. The simplified problem is:",
            "Students want to plant a lemon tree at their school, but the cold winter temperatures in Massachusetts would harm the tree. What is the best solution? (A) planting lemon trees together in a row (B) building a greenhouse for the lemon tree (C) giving extra fertilizer to the lemon tree in winter (D) using a stake to support the lemon tree during winter."
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
    return f"As a text readability expert specializing in science problems, your goal is to rephrase the problem so its readability level will match a given target Lexile score while ensuring the problem remains solvable with the same answer.\
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
           Now, here's a science problem for you to rephrase: {given_text}. \
           The problem's current Lexile score is: {cur_lexile_score}. \
           The target Lexile score for this problem is: {target_lexile}. \
           Please rephrase the problem to achieve the target Lexile score while preserving its original meaning. \
           Return just the rephrased problem. The rephrased problem is:"

def generate_fewshot_examples(target_lexile):
    fewshot_examples = []
    if target_lexile == 700:
        first_q = "A scientist studied layers of rock on the side of a cliff. In the top layer of rock, she found fossilized sand dunes. In the middle layer of rock, she found fossils of coral, clamshells, and shark teeth. In the bottom layer of rock, she found fossils of fern leaves. What is the correct order of the environments of the three layers, from oldest to youngest? (A) desert, ocean, forest (B) desert, forest, ocean (C) ocean, forest, desert (D) forest, ocean, desert."
        first_lexile = 924.263691722765
        second_q = "Alex looked at an electric toothbrush that had a plug with three metal prongs. Why are these prongs made out of metal? (A) Metal doesn't get hot and melt when you plug it into the outlet. (B) Metal is strong and is less likely to break when you plug it into the outlet. (C) Metal is an insulator and prevents shocks when you plug it into the outlet. (D) Metal is a conductor and completes a circuit when you plug it into the outlet."
        second_lexile = 833.7149497492361

        fewshot_examples = [
            first_q,
            first_lexile,
            target_detail_prompt(first_q, first_lexile, 700),
            "A scientist observed different layers of rock on a cliff. In the top layer, there were fossilized sand dunes. The middle layer contained fossils of coral, clamshells, and shark teeth. Lastly, the bottom layer held fossils of fern leaves. What is the correct order of the environments for these three layers, from oldest to youngest? (A) desert, ocean, forest (B) desert, forest, ocean (C) ocean, forest, desert (D) forest, ocean, desert.",
            "Your generated text Lexile Score is: 874.5489059040547\n Target Lexile Score is: 700. \n Currently syntax complexity is 752.8121904241725 ,lexical complexity is 870.8134402552392 and decodability complexity is 866.0630857838091. \n Please continue to rephrase the text to achieve the target Lexile score of 700 while preserving its original meaning. \n Return just the rephrased text. The rephrased text is:",
            "A scientist examined different layers of rock on a cliff. The top layer contained fossilized sand dunes. In the middle layer, there were fossils of coral, clamshells, and shark teeth. Finally, the bottom layer held fossils of fern leaves. What is the correct order of the environments for these three layers, from oldest to youngest? (A) desert, ocean, forest (B) desert, forest, ocean (C) ocean, forest, desert (D) forest, ocean, desert.",
            "Your generated text Lexile Score is: 870.5070397164636\n Target Lexile Score is: 700. \n Currently syntax complexity is 752.0897532404457 ,lexical complexity is 881.3427158265537 and decodability complexity is 871.7269251836202. \n Please continue to rephrase the text to achieve the target Lexile score of 700 while preserving its original meaning. \n Return just the rephrased text. The rephrased text is:",
            "A scientist examined different layers of rock on a cliff. The top layer contained fossilized sand dunes. In the middle layer, there were fossils of coral, clamshells, and shark teeth. Lastly, the bottom layer held fossils of fern leaves. What is the correct order of the environments for these three layers, from oldest to youngest? (A) desert, ocean, forest (B) desert, forest, ocean (C) ocean, forest, desert (D) forest, ocean, desert.",
            second_q,
            second_lexile,
            target_detail_prompt(second_q, second_lexile, 700),
            "Why are the prongs on an electric toothbrush made of metal? (A) Metal does not get hot and melt when it is plugged into the outlet. (B) Metal is strong and less likely to break when it is plugged into the outlet. (C) Metal insulates and prevents shocks when it is plugged into the outlet. (D) Metal conducts electricity and completes a circuit when it is plugged into the outlet.",
            "Your generated text Lexile Score is: 879.5770939478476\n Target Lexile Score is: 700. \n Currently syntax complexity is 923.4267344227137 ,lexical complexity is 881.5913138963425 and decodability complexity is 720.0743048232384. \n Please continue to rephrase the text to achieve the target Lexile score of 700 while preserving its original meaning. \n Return just the rephrased text. The rephrased text is:",
            "Why are the prongs on an electric toothbrush made of metal? (A) Metal does not heat up and melt when you plug it into the outlet. (B) Metal is strong and less likely to break when plugged into the outlet. (C) Metal acts as an insulator to prevent shocks when plugged into the outlet. (D) Metal conducts electricity and completes the circuit when plugged into the outlet.",
            "Your generated text Lexile Score is: 886.651269189613\n Target Lexile Score is: 700. \n Currently syntax complexity is 945.4541186758172 ,lexical complexity is 859.6984455076399 and decodability complexity is 772.4610405654931. \n Please continue to rephrase the text to achieve the target Lexile score of 700 while preserving its original meaning. \n Return just the rephrased text. The rephrased text is:",
            "Why are the prongs on an electric toothbrush made of metal? (A) Metal does not get hot and melt when you plug it into the outlet. (B) Metal is strong and less likely to break when you plug it into the outlet. (C) Metal acts as an insulator and prevents shocks when you plug it into the outlet. (D) Metal conducts electricity and completes a circuit when you plug it into the outlet."
        ]
    elif target_lexile == 900:
        first_p = "A scientist studied layers of rock on the side of a cliff. In the top layer of rock, she found fossilized sand dunes. In the middle layer of rock, she found fossils of coral, clamshells, and shark teeth. In the bottom layer of rock, she found fossils of fern leaves. What is the correct order of the environments of the three layers, from oldest to youngest? (A) desert, ocean, forest (B) desert, forest, ocean (C) ocean, forest, desert (D) forest, ocean, desert"
        first_lexile = 924.263691722765
        second_q = "Alex looked at an electric toothbrush that had a plug with three metal prongs. Why are these prongs made out of metal? (A) Metal doesn't get hot and melt when you plug it into the outlet. (B) Metal is strong and is less likely to break when you plug it into the outlet. (C) Metal is an insulator and prevents shocks when you plug it into the outlet. (D) Metal is a conductor and completes a circuit when you plug it into the outlet."
        second_lexile = 833.7149497492361

        fewshot_examples = [
            first_p,
            first_lexile,
            target_detail_prompt(first_q, first_lexile, 900),
            "A scientist examined rock layers on a cliff. In the highest layer, she discovered fossilized sand dunes. In the middle layer, she found fossils of coral, clamshells, and shark teeth. In the lowest layer, she uncovered fossils of fern leaves. What is the correct sequence of environments for these three layers, starting with the oldest? (A) desert, ocean, forest (B) desert, forest, ocean (C) ocean, forest, desert (D) forest, ocean, desert.",
            "Your generated text Lexile Score is: 898.0399793096465\n Target Lexile Score is: 900. \n Currently syntax complexity is 773.0228958129949 ,lexical complexity is 887.2572979777045 and decodability complexity is 879.5486229793689. \n Please continue to rephrase the text to achieve the target Lexile score of 900 while preserving its original meaning. \n Return just the rephrased text. The rephrased text is:",
            "A scientist examined the layers of rock on a cliff. In the top layer, she discovered fossilized sand dunes. In the middle layer, she found fossils of coral, clamshells, and shark teeth. In the bottom layer, she uncovered fossils of fern leaves. What is the correct order of the environments for these three layers, starting with the oldest? (A) desert, ocean, forest (B) desert, forest, ocean (C) ocean, forest, desert (D) forest, ocean, desert.",
            "Your generated text Lexile Score is: 860.8538616221617\n Target Lexile Score is: 900. \n Currently syntax complexity is 759.222350860882 ,lexical complexity is 882.3847790442502 and decodability complexity is 876.8418315700185. \n Please continue to rephrase the text to achieve the target Lexile score of 900 while preserving its original meaning. \n Return just the rephrased text. The rephrased text is:",
            "A scientist examined the various layers of rock on the side of a cliff. In the uppermost layer, she made a fascinating discovery of fossilized sand dunes. Moving to the middle layer, she made further exciting findings of fossilized coral, clamshells, and even shark teeth. Finally, in the lowermost layer, she unearthed the remnants of fern leaves from a bygone era. Can you determine the correct order of these environments, from oldest to youngest? Choose from the options: (A) desert, ocean, forest (B) desert, forest, ocean (C) ocean, forest, desert (D) forest, ocean, desert",
            second_q,
            second_lexile,
            target_detail_prompt(second_q, second_lexile, 900),
            "Why are metal prongs used in the plug of an electric toothbrush? (A) Metal prongs are resistant to heat and do not melt when plugged into an outlet. (B) Metal prongs are durable and less likely to break when plugged into an outlet. (C) Metal prongs are not insulators and do not cause shocks when plugged into an outlet. (D) Metal prongs are conductors that complete a circuit when plugged into an outlet.",
            "Your generated text Lexile Score is: 962.5852529972138\n Target Lexile Score is: 900. \n Currently syntax complexity is 1001.5714012847806 ,lexical complexity is 949.1874107417542 and decodability complexity is 805.1281327903735. \n Please continue to rephrase the text to achieve the target Lexile score of 900 while preserving its original meaning. \n Return just the rephrased text. The rephrased text is:",
            "Why are metal prongs used in the plug of an electric toothbrush? (A) Metal prongs are heat-resistant and won't melt when plugged into an outlet. (B) Metal prongs are strong and less likely to break when plugged into an outlet. (C) Metal prongs are not insulators and prevent shocks when plugged into an outlet. (D) Metal prongs are conductors that complete the circuit when plugged into an outlet",
            "Your generated text Lexile Score is: 986.0096493837112\n Target Lexile Score is: 900. \n Currently syntax complexity is 981.1883770274696 ,lexical complexity is 926.27652466105 and decodability complexity is 845.3357746031489. \n Please continue to rephrase the text to achieve the target Lexile score of 900 while preserving its original meaning. \n Return just the rephrased text. The rephrased text is:",
            "Why are metal prongs used in the plug of an electric toothbrush? (A) Metal prongs are heat-resistant and won't melt when inserted into an outlet. (B) Metal prongs are durable and less likely to break when inserted into an outlet. (C) Metal prongs are not insulators and provide protection against electrical shocks when inserted into an outlet. (D) Metal prongs are conductors that complete the electrical circuit when inserted into an outlet."
        ]
    elif target_lexile == 1200:
        first_p = "A scientist studied layers of rock on the side of a cliff. In the top layer of rock, she found fossilized sand dunes. In the middle layer of rock, she found fossils of coral, clamshells, and shark teeth. In the bottom layer of rock, she found fossils of fern leaves. What is the correct order of the environments of the three layers, from oldest to youngest? (A) desert, ocean, forest (B) desert, forest, ocean (C) ocean, forest, desert (D) forest, ocean, desert."
        first_lexile = 924.263691722765
        second_p = "In the early 1900s, farmers plowed large areas of land to plant crops. This removed the natural grasses and trees. These plants had deep roots that kept the soil in place. In the 1930s, there was a long drought, so crops would not grow. This exposed large areas of bare soil. The wind picked up a large amount of soil and blew it away. After the drought ended, the U.S. government encouraged farmers to change their farming practices to prevent this from happening again. Which practice would best help the soil stay in place? (A) planting only natural grasses and corn in the fields (B) planting soybeans and corn in fields next to fields with cattle (C) planting trees and grasses in areas between fields with crops (D) building pipelines to carry large amounts of water to use in sprinklers in the fields"
        second_lexile = 881.2064663150644

        fewshot_examples = [
            first_p,
            first_lexile,
            target_detail_prompt(first_q, first_lexile, 1200),
            "A scientist examined rock layers on a cliff. The top layer contained fossilized sand dunes, the middle layer contained fossils of coral, clamshells, and shark teeth, and the bottom layer contained fossils of fern leaves. What is the correct order of the environments for these three layers, from oldest to youngest? (A) desert, ocean, forest (B) desert, forest, ocean (C) ocean, forest, desert (D) forest, ocean, desert.",
            "Your generated text Lexile Score is: 1154.147897818295\n Target Lexile Score is: 1200. \n Currently syntax complexity is 918.8598876004218 ,lexical complexity is 1161.0949308483946 and decodability complexity is 874.2559686828984. \n Please continue to rephrase the text to achieve the target Lexile score of 1200 while preserving its original meaning. \n Return just the rephrased text. The rephrased text is:",
            "A scientist examined the different layers of rock on a cliff to understand their history. In the uppermost layer, she discovered fossilized sand dunes. Moving to the middle layer, she found fascinating fossils of coral, clamshells, and shark teeth. Finally, in the bottom layer, she encountered preserved fern leaves. Now, can you determine the correct chronological order of the environments represented by these three layers? Choose the option that goes from the oldest to the youngest: (A) desert, ocean, forest (B) desert, forest, ocean (C) ocean, forest, desert (D) forest, ocean, desert.",
            "Your generated text Lexile Score is: 1120.941233282606\n Target Lexile Score is: 1200. \n Currently syntax complexity is 1017.3004917130328 ,lexical complexity is 1144.9241176646124 and decodability complexity is 839.0474842557161. \n Please continue to rephrase the text to achieve the target Lexile score of 1200 while preserving its original meaning. \n Return just the rephrased text. The rephrased text is:",
            "A scientist conducted a study on the layers of rock found on a cliff to understand their history. In the uppermost layer, she made an intriguing discovery of fossilized sand dunes. As she moved to the middle layer, she encountered fascinating fossils including coral, clamshells, and shark teeth. Finally, in the bottommost layer, she unearthed fossils of fern leaves. Can you determine the correct sequence of environments represented by these three layers, from oldest to youngest? Choose the option that includes the environments in the correct order: (A) desert, ocean, forest (B) desert, forest, ocean (C) ocean, forest, desert (D) forest, ocean, desert.",
            second_p,
            second_lexile,
            target_detail_prompt(second_q, second_lexile, 1200),
            "During the early 1900s, farmers engaged in extensive plowing of land in order to cultivate crops. Consequently, the natural grasses and trees were eradicated, which were crucial in holding the soil intact due to their deep-rooted nature. In the 1930s, a prolonged drought prevailed, making it impossible for crops to flourish. Consequently, vast areas of soil were left exposed. Subsequently, strong winds picked up substantial amounts of soil and carried it away. Following the end of the drought, the U.S. government encouraged farmers to adopt alternative farming practices to prevent a recurrence of this situation. Which of the following practices would be most effective in ensuring soil stability? (A) Exclusively planting natural grasses and corn in the fields (B) Planting soybeans and",
            "Your generated text Lexile Score is: 1035.7853932689586\n Target Lexile Score is: 1200. \n Currently syntax complexity is 962.0042371590818 ,lexical complexity is 1082.4886499686054 and decodability complexity is 814.7551774656057. \n Please continue to rephrase the text to achieve the target Lexile score of 1200 while preserving its original meaning. \n Return just the rephrased text. The rephrased text is:",
            "In the early 1900s, farmers extensively plowed large areas of land to plant crops which resulted in the removal of natural grasses and trees. These plants had deep roots that played a vital role in preventing soil erosion. However, in the 1930s, a prolonged drought hindered crop growth, exposing vast areas of bare soil. Strong winds then carried away substantial amounts of soil. To prevent a recurrence of this problem, the U.S. government encouraged farmers to modify their farming practices. Which practice would be most effective in preserving soil stability? (A) Planting a combination of natural grasses and corn in the fields (B) Planting soybeans and corn in fields adjacent to cattle fields (C) Planting trees and grasses in areas between crop fields (D)",
            "Your generated text Lexile Score is: 1203.2311768954416\n Target Lexile Score is: 1200. \n Currently syntax complexity is 1134.6046068489409 ,lexical complexity is 1114.0858707646526 and decodability complexity is 869.3393488089839. \n Please continue to rephrase the text to achieve the target Lexile score of 1200 while preserving its original meaning. \n Return just the rephrased text. The rephrased text is:",
            "During the early 1900s, farmers extensively plowed vast areas of land to cultivate crops. This resulted in the removal of natural grasses and trees, which played a crucial role in preventing soil erosion due to their deep roots. However, in the 1930s, a prolonged drought occurred, causing crops to fail and leaving large areas of bare soil exposed. Strong winds then carried away significant amounts of soil. To prevent a recurrence of this problem, the U.S. government encouraged farmers to modify their farming practices. Which of the following practices would best help preserve the soil? (A) Planting a combination of natural grasses and corn in the fields (B) Planting soybeans and corn in fields adjacent to cattle fields (C) Planting trees and grasses in areas between"
        ]
    else:
        print("We don't have examples for that lexile score.")
    return fewshot_examples

def target_exp_initial_prompt(prompt_detail, given_text, cur_lexile_score, target_lexile):
    messages = []
    prompt_detail = prompt_detail.lower()
    prompt = ""
    if prompt_detail == "base":
        prompt = f"As a text readability expert specializing in science questions, your goal is to adjust the text's readability to match the target Lexile score while ensuring it remains solvable with the same answer. \
        Here's a science problem for you to adjust: {given_text}.\
        The target Lexile score for this problem is: {target_lexile}.\
        Please rephrase the text to achieve the target Lexile score while preserving its original meaning.\n The rephrased text:"
    elif prompt_detail == "knowledge":
        prompt = f"As a text readability expert specializing in science questions, your goal is to adjust the text's readability to match the target Lexile score while ensuring it remains solvable with the same answer. \
        Consider that Lexile takes into account three main factors:\
        1. Syntax complexity - Determined by factors such as the number of words and characters, parsing tree depth, maximum nesting level, punctuation count, and the number of entity and POS tags.\
        2. Lexical complexity - Assessed based on the number of words in the DallChall list, syllables count, the number of difficult words (according to syllables), and Kuperman Age of Acquisition (AoA).\
        3. Decodability complexity - Calculated using metrics like type-token ratio (ttr), letter sound discrepancy, and average grapheme-phoneme correspondences (GPCs) probability.\
        Here's a science problem for you to adjust: {given_text}.\
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
        prompt = f"As a text simplification agent specialized in science problems, your goal is to enhance the readability of science questions while ensuring they remain solvable with the same answer. \
               Let's focus on {category} complexity for this task. \
               Here's a science problem for you to simplify: {given_text}.\
               Please simplify the text while preserving its original meaning with a focus on reducing {category} complexity. \n The simplified text:"
    elif prompt_detail == "knowledge":
        G_category_exp = category_exp(category)
        prompt = f"As a text simplification agent specialized in science problems, your goal is to enhance the readability of science questions while ensuring they remain solvable with the same answer. \
               Let's focus on {category} complexity for this task. \
               {G_category_exp} \
               Here's a science problem for you to simplify: {given_text}.\
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