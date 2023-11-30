import openai
import time
import re

openai_model = "gpt-4"

ANS_RE = re.compile(r"#### (\-?[0-9\.\,]+)")
INVALID_ANS = "[invalid]"

def extract_answer(completion):
    match = ANS_RE.search(completion)
    if match:
        match_str = match.group(1).strip()
        match_str = match_str.replace(",", "")
        return match_str
    else:
        return INVALID_ANS

def is_correct(model_completion, gt_example):
    gt_answer = extract_answer(gt_example["answer"])
    assert gt_answer != INVALID_ANS
    print(extract_answer(model_completion) == gt_answer)
    return extract_answer(model_completion) == gt_answer
    

def ask_gpt_to_verify(question):
    # Define your prompt based on the example you gave
    messages = [
        {
            "role": "user",
            "content": """
                   ”
                   Assist in solving the following grade school math problems from the GSM8K dataset. These problems are typically solvable by middle school students and involve 2 to 8 steps using basic arithmetic operations.

                   Essential Format:

                   Start by listing the logical steps taken to solve the problem.
                   Conclude with the final answer, which must be placed after the "####" marker.
                   Example:
                   Q:Natalia sold clips to 48 of her friends in April, and then she sold half as many clips in May. How many clips did Natalia sell altogether in April and May?
                   Ans:Natalia sold 48/2 = <<48/2=24>>24 clips in May. Natalia sold 48+24 = <<48+24=72>>72 clips altogether in April and May. #### 72
                   - - -
                   Q:The profit from a business transaction is shared among 2 business partners, Mike and Johnson in the ratio 2:5 respectively. If Johnson got $2500, how much will Mike have after spending some of his share on a shirt that costs $200?
                   Ans:According to the ratio, for every 5 parts that Johnson gets, Mike gets 2 parts Since Johnson got $2500, each part is therefore $2500/5 = $<<2500/5=500>>500 Mike will get 2*$500 = $<<2*500=1000>>1000 After buying the shirt he will have $1000-$200 = $<<1000-200=800>>800 left #### 800
                   - - -
                   Q:It takes Roque two hours to walk to work and one hour to ride his bike to work. Roque walks to and from work three times a week and rides his bike to and from work twice a week. How many hours in total does he take to get to and from work a week with walking and biking?
                   Ans:Roque takes 2*3 = <<2*3=6>>6 hours a week to walk to work. Roque takes 6*2 = <<6*2=12>>12 hours a week to walk to and from work. Roque takes 1*2 = <<1*2=2>>2 hours a week to bike to work. Roque takes 2*2 = <<2*2=4>>4 hours a week to bike to and from work. In total, Roque takes 12+4 = <<12+4=16>>16 hour a week to go to and from work. #### 16
                   - - -
                   Q:Tim rides his bike back and forth to work for each of his 5 workdays. His work is 20 miles away. He also goes for a weekend bike ride of 200 miles. If he can bike at 25 mph how much time does he spend biking a week?
                   Ans:He bikes 20*2=<<20*2=40>>40 miles each day for work So he bikes 40*5=<<40*5=200>>200 miles for work That means he bikes a total of 200+200=<<200+200=400>>400 miles for work So he bikes a total of 400/25=<<400/25=16>>16 hours #### 16
                   - - -
                   Q:Bella bought stamps at the post office. Some of the stamps had a snowflake design, some had a truck design, and some had a rose design. Bella bought 11 snowflake stamps. She bought 9 more truck stamps than snowflake stamps, and 13 fewer rose stamps than truck stamps. How many stamps did Bella buy in all?
                   Ans:The number of truck stamps is 11 + 9 = <<11+9=20>>20. The number of rose stamps is 20 − 13 = <<20-13=7>>7. Bella bought 11 + 20 + 7 = <<11+20+7=38>>38 stamps in all. #### 38
                   - - -
                   Q:Each bird eats 12 beetles per day, each snake eats 3 birds per day, and each jaguar eats 5 snakes per day. If there are 6 jaguars in a forest, how many beetles are eaten each day?
                   Ans:First find the total number of snakes eaten: 5 snakes/jaguar * 6 jaguars = <<5*6=30>>30 snakes Then find the total number of birds eaten per day: 30 snakes * 3 birds/snake = <<30*3=90>>90 snakes Then multiply the number of snakes by the number of beetles per snake to find the total number of beetles eaten per day: 90 snakes * 12 beetles/snake = <<90*12=1080>>1080 beetles #### 1080
                   - - -
                   Q:Samantha’s last name has three fewer letters than Bobbie’s last name. If Bobbie took two letters off her last name, she would have a last name twice the length of Jamie’s. Jamie’s full name is Jamie Grey. How many letters are in Samantha’s last name?
                   Ans:There are 4 letters in Jamie’s last name, so Bobbie’s name is 4*2 +2 = <<4*2+2=10>>10 letters long. Samantha’s last name is 3 letters shorter than Bobbie’s, so there are 10 - 3 = <<10-3=7>>7 letters in Samantha’s last name. #### 7
                   - - -
                   Q:Ann's favorite store was having a summer clearance. For $75 she bought 5 pairs of shorts for $7 each and 2 pairs of shoes for $10 each. She also bought 4 tops, all at the same price. How much did each top cost?
                   Ans:She bought 5 shorts at $7 each so 5*7=$<<5*7=35>>35 She bought 2 pair of shoes at $10 each so 2*10=$<<2*10=20>>20 The shorts and shoes cost her 35+20 = $<<35+20=55>>55 We know she spent 75 total and the shorts and shoes cost $55 which left a difference of 75-55 = $<<75-55=20>>20 She bought 4 tops for a total of $20 so 20/4 = $5 #### 5
                   - - -
                   Q:Mary does her grocery shopping on Saturday. She does her shopping only at a specific store where she is allowed a credit of $100, which must be paid in full before her next shopping trip. That week she spent the full credit limit and paid $15 of it on Tuesday and $23 of it on Thursday. How much credit will Mary need to pay before her next shopping trip?
                   Ans:So far, Mary has paid back $15 +$23=$<<15+23=38>>38 of the credit. So she still needs to pay $100-$38=$<<100-38=62>>62 #### 62
                   - - -
                   Q:Ralph is going to practice playing tennis with a tennis ball machine that shoots out tennis balls for Ralph to hit. He loads up the machine with 175 tennis balls to start with. Out of the first 100 balls, he manages to hit 2/5 of them. Of the next 75 tennis balls, he manages to hit 1/3 of them. Out of all the tennis balls, how many did Ralph not hit?
                   Ans:Out of the first 100 balls, Ralph was able to hit 2/5 of them and not able to hit 3/5 of them, 3/5 x 100 = 60 tennis balls Ralph didn't hit. Out of the next 75 balls, Ralph was able to hit 1/3 of them and not able to hit 2/3 of them, 2/3 x 75 = 50 tennis balls that Ralph didn't hit. Combined, Ralph was not able to hit 60 + 50 = <<60+50=110>>110 tennis balls Ralph didn't hit. #### 110

                   Please provide solutions for the following question using the above format:
                   Q:{}
                   """.format(question)
        }
    ]
    for attempt in range(3):
        try:
            response = openai.ChatCompletion.create(
                model=openai_model,
                messages=messages,
            )
            return response.choices[0].message.content
        except openai.error.Timeout as e:
            print(f"Request timed out (Attempt {attempt + 1}/{3}). Retrying in {5} seconds...")
            time.sleep(5)
            continue
    return "None #### 0"

def is_solvable(simplified_text, ans):
    model_completion = ask_gpt_to_verify(simplified_text)
    return is_correct(model_completion, {"answer": f"{ans}"})

def extract_question(text):
    # Split the text into sentences
    sentences = re.split(r'(?<!\w\.\w.)(?<![A-Z][a-z]\.)(?<=\.|\?|\!)\s', text)

    # Filter out sentences containing the word "Lexile"
    question_sentences = [sentence for sentence in sentences if "Lexile" not in sentence and "syntax" not in sentence and "lexical" not in sentence]

    # Join the remaining sentences to form the question
    question = ' '.join(question_sentences)

    return question