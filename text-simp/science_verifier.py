import openai
import time
import re

openai_model = "gpt-4"

ANS_RE = re.compile(r"#### (\-?[0-9\.\,]+)")
INVALID_ANS = "[invalid]"

def extract_answer(completion):
    match = re.findall("[A-Z]\.|\([A-Z]\)|[A-Z] -|[A-Z]\)", completion)
    if match:
        match_str = re.findall("[a-zA-Z]", match[0])[0]
        return match_str
    else:
        return INVALID_ANS

def is_correct(correct_answer, gpt_answer):
    print(gpt_answer)
    print(correct_answer)
    print(extract_answer(gpt_answer) == correct_answer)
    print("-------------------------------------")
    return extract_answer(gpt_answer) == correct_answer

def ask_gpt_to_verify(question):
    # Define your prompt based on the example you gave
    answer_question_prompt = [
        {"role": "system", "content": "You are a helpful assistant."},
        {"role": "user", "content": "Q: People need vitamin D to help their bones get enough calcium so that the bones can be strong. People can get vitamin D from milk, fish, and mushrooms. People\u2019s bodies can also make vitamin D when their skin absorbs light from the Sun. Which situation will most likely cause a person\u2019s bones to become weak? A. The person spends a lot of time outside B. The person avoids foods with vitamin D C. The person eats cereal with milk for breakfast each morning D. The person eats lots of fish that provide vitamin D"},
        {"role": "assistant", "content": "(B) The person avoids foods with vitamin D."},
        {"role": "user", "content": "Q: In the early 1900s, farmers plowed large areas of land to plant crops. This removed the natural grasses and trees. These plants had deep roots that kept the soil in place. In the 1930s, there was a long drought, so crops would not grow. This exposed large areas of bare soil. The wind picked up a large amount of soil and blew it away. After the drought ended, the U.S. government encouraged farmers to change their farming practices to prevent this from happening again. Which practice would best help the soil stay in place? A. planting only natural grasses and corn in the fields B. planting soybeans and corn in fields next to fields with cattle C. planting trees and grasses in areas between fields with crops D. building pipelines to carry large amounts of water to use in sprinklers in the fields"},
        {"role": "assistant", "content": "(C) planting trees and grasses in areas between fields with crops"},
        {"role": "user", "content": f"Q: {question}"},
    ]

    for attempt in range(3):
        try:
            response = openai.ChatCompletion.create(
                model=openai_model,
                messages=answer_question_prompt,
            )
            return response.choices[0].message.content
        except openai.error.Timeout as e:
            print(f"Request timed out (Attempt {attempt + 1}/{3}). Retrying in {5} seconds...")
            time.sleep(5)
            continue
    return "None"

def is_solvable(simplified_text, ans):
    model_completion = ask_gpt_to_verify(simplified_text)
    return is_correct(ans, model_completion)