from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import bs4
from time import sleep
import pandas as pd
import re
from dotenv import load_dotenv
import os

driver = webdriver.Chrome() #webdriver.Edge()

# These are all the pages from which I have already extracted the texts.
USED_LINKS = {"2th_grade": ["https://www.readworks.org/find-content#!contentTab:search/q:/g:18/t:/f:0/pt:/features:/",
                        "https://www.readworks.org/find-content#!contentTab:search/q:/g:18/t:/f:1/pt:/features:/",
                        "https://www.readworks.org/find-content#!contentTab:search/q:/g:18/t:/f:2/pt:/features:/wc:200,3000/",
                        "https://www.readworks.org/find-content#!contentTab:search/q:/g:18/t:/f:3/pt:/features:/wc:200,3000/",
                        "https://www.readworks.org/find-content#!contentTab:search/q:/g:18/t:/f:4/pt:/features:/wc:200,3000/",
                        "https://www.readworks.org/find-content#!contentTab:search/q:/g:18/t:/f:5/pt:/features:/wc:200,3000/",
                        "https://www.readworks.org/find-content#!contentTab:search/q:/g:18/t:/f:6/pt:/features:/wc:200,3000/",
                        "https://www.readworks.org/find-content#!contentTab:search/q:/g:18/t:/f:7/pt:/features:/wc:200,3000/"
                            ],
              "3th_grade": ["https://www.readworks.org/find-content#!contentTab:search/q:/g:19/t:/f:2/pt:/features:/",
                        "https://www.readworks.org/find-content#!contentTab:search/q:/g:19/t:/f:3/pt:/features:/",
                        "https://www.readworks.org/find-content#!contentTab:search/q:/g:19/t:/f:2/pt:/features:/wc:300,3000/",
                        "https://www.readworks.org/find-content#!contentTab:search/q:/g:19/t:/f:3/pt:/features:/wc:300,3000/",
                        "https://www.readworks.org/find-content#!contentTab:search/q:/g:19/t:/f:4/pt:/features:/wc:300,3000/",
                        "https://www.readworks.org/find-content#!contentTab:search/q:/g:19/t:/f:5/pt:/features:/wc:300,3000/",
                        "https://www.readworks.org/find-content#!contentTab:search/q:/g:19/t:/f:6/pt:/features:/wc:300,3000/",
                        "https://www.readworks.org/find-content#!contentTab:search/q:/g:19/t:/f:7/pt:/features:/wc:300,3000/"
                            ],
              "4th_grade": ["https://www.readworks.org/find-content#!contentTab:search/q:/g:20/t:/f:0/l:150,2200/pt:A/features:/",
                        "https://www.readworks.org/find-content#!contentTab:search/q:/g:20/t:/f:1/l:150,2200/pt:A/features:/",
                        "https://www.readworks.org/find-content#!contentTab:search/q:/g:20/t:/f:2/l:150,2200/pt:A/features:/",
                        "https://www.readworks.org/find-content#!contentTab:search/q:/g:20/t:/f:3/l:150,2200/pt:A/features:/",
                        "https://www.readworks.org/find-content#!contentTab:search/q:/g:20/t:/f:4/l:150,2200/pt:A/features:/",
                        "https://www.readworks.org/find-content#!contentTab:search/q:/g:20/t:/f:5/l:150,2200/pt:A/features:/",
                        "https://www.readworks.org/find-content#!contentTab:search/q:/g:20/t:/f:6/l:150,2200/pt:A/features:/",
                        "https://www.readworks.org/find-content#!contentTab:search/q:/g:20/t:/f:7/l:150,2200/pt:A/features:/"
                            ],
              "5th_grade": ["https://www.readworks.org/find-content#!contentTab:search/q:/g:21/t:/f:0/l:150,2200/pt:/sr:false/features:/",
                        "https://www.readworks.org/find-content#!contentTab:search/q:/g:21/t:/f:1/l:150,2200/pt:/sr:false/features:/",
                        "https://www.readworks.org/find-content#!contentTab:search/q:/g:21/t:/f:2/l:150,2200/pt:/sr:false/features:/",
                        "https://www.readworks.org/find-content#!contentTab:search/q:/g:21/t:/f:3/l:150,2200/pt:/sr:false/features:/",
                        "https://www.readworks.org/find-content#!contentTab:search/q:/g:21/t:/f:4/l:150,2200/pt:/sr:false/features:/",
                        "https://www.readworks.org/find-content#!contentTab:search/q:/g:21/t:/f:5/l:150,2200/pt:/sr:false/features:/",
                        "https://www.readworks.org/find-content#!contentTab:search/q:/g:21/t:/f:6/l:150,2200/pt:/sr:false/features:/",
                        "https://www.readworks.org/find-content#!contentTab:search/q:/g:21/t:/f:7/l:150,2200/pt:/sr:false/features:/"
                            ],
              "6th_grade": ["https://www.readworks.org/find-content#!contentTab:search/q:/g:22/t:/f:0/l:150,2200/pt:/sr:false/features:/",
                        "https://www.readworks.org/find-content#!contentTab:search/q:/g:22/t:/f:1/l:150,2200/pt:/sr:false/features:/",
                        "https://www.readworks.org/find-content#!contentTab:search/q:/g:22/t:/f:2/l:150,2200/pt:/sr:false/features:/",
                        "https://www.readworks.org/find-content#!contentTab:search/q:/g:22/t:/f:3/l:150,2200/pt:/sr:false/features:/",
                        "https://www.readworks.org/find-content#!contentTab:search/q:/g:22/t:/f:4/l:150,2200/pt:/sr:false/features:/",
                        "https://www.readworks.org/find-content#!contentTab:search/q:/g:22/t:/f:5/l:150,2200/pt:/sr:false/features:/",
                        "https://www.readworks.org/find-content#!contentTab:search/q:/g:22/t:/f:6/l:150,2200/pt:/sr:false/features:/",
                        "https://www.readworks.org/find-content#!contentTab:search/q:/g:22/t:/f:7/l:150,2200/pt:/sr:false/features:/"
                            ],
              }

def log_in():
    # The website requires login access to view the texts
    # The function execute the login process

    login_button_xpath = "//button[contains(@class, 'login-button')]"
    login_button_js = f"document.evaluate(\"{login_button_xpath}\", document, null, XPathResult.FIRST_ORDERED_NODE_TYPE, null).singleNodeValue.click();"
    driver.execute_script(login_button_js)

    # Wait for the login modal to appear
    modal_window = WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.ID, 'teacher-login-modal')))
    educator_choice_xpath = "//button[contains(@class, 'teacher-choice')]/span[text()='Educator/Parent']"
    educator_choice_js = f"document.evaluate(\"{educator_choice_xpath}\", document, null, XPathResult.FIRST_ORDERED_NODE_TYPE, null).singleNodeValue.click();"
    driver.execute_script(educator_choice_js)
    # print(soup.prettify())
    email_field = WebDriverWait(modal_window, 10).until(EC.visibility_of_element_located((By.ID, 'teacher-login-modal-email')))
    password_field = modal_window.find_element(By.ID, 'teacher-login-modal-password')

    load_dotenv()

    web_scrapping_id = os.getenv("WEB_SCRAPPING_ID")
    web_scrapping_password = os.getenv("WEB_SCRAPPING_PASSWORD")
    # Enter your email and password
    email_field.send_keys(web_scrapping_id)
    password_field.send_keys(web_scrapping_password)

    # Submit the form
    password_field.send_keys(Keys.RETURN)

def clean_content(article_content):
    # Clean the content from irrelevant text before saving it
    article_content = article_content
    sentences = article_content.split("©", 1)
    if len(sentences) == 1:
        sentences = article_content.split("This article from", 1)
    cleaned_text = sentences[0]
    return cleaned_text

def extract_lexile_score(lexile):
    # The function extracts the Lexile score as an integer from the string
    numbers = re.findall(r'\d+', lexile)
    if numbers:
        return int(numbers[0])
    else:
        return None  # Return None if no numbers were found

def extract_text_information(df):
    # The function extracts the article title, grade, Lexile score and content from specific article page

    current_page_soup = bs4.BeautifulSoup(driver.page_source, 'html.parser')
    # print(current_page_soup.prettify())

    # Extract the title
    title_element = current_page_soup.find('h1', class_='main-header-title')
    article_title = title_element.text.strip() if title_element else "Title not found"

    # Extract the Grade and Lexile elements
    grade_li = current_page_soup.find('li', string=lambda text: text and "Grade:" in text)
    grade = grade_li.text.strip().split(': ')[1] if grade_li else "Grade not found"
    lexile_li = current_page_soup.find('li', string=lambda text: text and "Lexile:" in text)
    lexile = lexile_li.text.strip().split(': ')[1] if lexile_li else "Lexile not found"
    Lexile_score = extract_lexile_score(lexile)
    if Lexile_score is None:
        return df

    # Extract the article content
    content_paragraphs = current_page_soup.find_all('p')
    filtered_paragraphs = [p.get_text(strip=True) for p in content_paragraphs if
                           not p.get_text(strip=True).startswith(("Photograph", "photograph", "Photo", "photo", "image","Image", "By", "Copyright", "Text and image provided","The text and image",
                                                                  "This text is", "These conservation efforts", "-", "iStock", "The text","U.S"))]
    article_content = "\n".join(filtered_paragraphs)
    article_content = clean_content(article_content)

    dict_format = {'Title': article_title , 'Content': article_content, 'Lexile': Lexile_score, 'Grade': grade}
    df = pd.concat([df, pd.DataFrame([dict_format])], ignore_index=True)
    return df

def extract_all_texts_from_page(page_path, df,log_in_needed):
    # Each page contains approximately 20 texts. The function extracts all the texts from a specific page
    driver.get(page_path)
    if log_in_needed:
        log_in()
    sleep(1)
    elements = driver.find_elements(By.CLASS_NAME, 'article-result-content')
    for i in range(0, len(elements)):
        try:
            elements[i].click()
            sleep(1)
            df = extract_text_information(df)
            driver.back()
            sleep(2)
            elements = driver.find_elements(By.CLASS_NAME, 'article-result-content')
        except:
            print("An Exception Occured")
            continue
    return df

def run_initial_web_scraping():
    # The function runs the web scraping process and generates an XLSX file.
    # It should be used only for the initial setup, and afterward, utilize the function below.

    new_df = pd.DataFrame(columns=["Title", "Content", "Lexile", "Grade"])
    pages_list_2th_grade = [
        "https://www.readworks.org/find-content#!contentTab:search/q:/g:18/t:/f:0/pt:/features:/",
        "https://www.readworks.org/find-content#!contentTab:search/q:/g:18/t:/f:1/pt:/features:/"]
    pages_list_3th_grade = [
        "https://www.readworks.org/find-content#!contentTab:search/q:/g:19/t:/f:2/pt:/features:/",
        "https://www.readworks.org/find-content#!contentTab:search/q:/g:19/t:/f:3/pt:/features:/"]
    pages_list_4th_grade = [
        "https://www.readworks.org/find-content#!contentTab:search/q:/g:20/t:/f:0/l:150,2200/pt:A/features:/",
        "https://www.readworks.org/find-content#!contentTab:search/q:/g:20/t:/f:1/l:150,2200/pt:A/features:/"]
    pages_list_5th_grade = [
        "https://www.readworks.org/find-content#!contentTab:search/q:/g:21/t:/f:0/l:150,2200/pt:/sr:false/features:/",
        "https://www.readworks.org/find-content#!contentTab:search/q:/g:21/t:/f:1/l:150,2200/pt:/sr:false/features:/"]
    pages_list_6th_grade = [
        "https://www.readworks.org/find-content#!contentTab:search/q:/g:22/t:/f:0/l:150,2200/pt:/sr:false/features:/",
        "https://www.readworks.org/find-content#!contentTab:search/q:/g:22/t:/f:1/l:150,2200/pt:/sr:false/features:/"]

    pages_total_list = pages_list_2th_grade + pages_list_3th_grade + pages_list_4th_grade + pages_list_5th_grade + pages_list_6th_grade
    log_in_needed = True
    for page in pages_total_list:
        print("page")
        new_df = extract_all_texts_from_page(page, new_df, log_in_needed)
        log_in_needed = False
    output_file = 'trained_models/linguistic_features/datasets/lexile_dataset.xlsx'
    new_df.to_excel(output_file, index=False)
'''
def test():
    df = pd.DataFrame(columns=["Title", "Content", "Lexile", "Grade"])
    path = os.path.abspath("datasets")
    path += '/lexile_dataset.xlsx'
    print(path)
    #output_file = 'trained_models/linguistic_features/datasets/Lexile_dataset_updated.xlsx'
    df.to_excel(path, index=False)
'''

def add_more_data(df,pages_new_list):
    # The function adds more data to the existing dataset file.
    # To add more data to the database, execute this function.
    log_in_needed = True
    for page in pages_new_list:
        print("page")
        df = extract_all_texts_from_page(page, df, log_in_needed)
        log_in_needed = False
    output_file = os.path.abspath("datasets")
    output_file += '/lexile_dataset.xlsx'
    df.to_excel(output_file, index=False)
'''
if __name__ == '__main__':

    dataset_path = 'trained_models/linguistic_features/datasets/Lexile_dataset_updated.xlsx'
    df = pd.read_excel(dataset_path)
    pages_new_list = [] # Add here the new pages to scrape
    add_more_data(df,pages_new_list)
    run_initial_web_scraping()

'''