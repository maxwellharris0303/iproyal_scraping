from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait
from selenium.common.exceptions import *
from time import sleep
from urllib.parse import urlparse
import json

def scrape(url, index):
    options = webdriver.ChromeOptions()
    options.add_argument('--headless=new')
    driver = webdriver.Chrome(options=options)
    driver.maximize_window()
    driver.get(url)

    sleep(3)
    meta_title = driver.find_element(By.CSS_SELECTOR, "meta[name=\"twitter:title\"]").get_attribute("content")
    print(f"Meta title: {meta_title}")
    meta_description = driver.find_element(By.CSS_SELECTOR, "meta[name=\"description\"]").get_attribute("content")
    print(f"Meta description: {meta_description}")

    brand = driver.find_element(By.CSS_SELECTOR, "a[class=\"!text-brand-400\"]").text
    print(f"Brand: {brand}")
    h1 = driver.find_element(By.CSS_SELECTOR, "h1[class=\"tp-headline-m lg:tp-headline-l lg:max-w-[600px]\"]").text
    print(f"H1: {h1}")

    jumbotron_text = driver.find_element(By.CSS_SELECTOR, "div[class=\"lg:tp-subheadline\"]").text
    print(f"Jumbotron text: {jumbotron_text}")
    try:
        jumbotron_image = driver.find_element(By.CSS_SELECTOR, "img[class=\"w-full h-full hidden lg:block\"]").get_attribute('src')
    except:
        jumbotron_image = driver.find_element(By.CSS_SELECTOR, "img[class=\"w-full h-full object-contain\"]").get_attribute('src')
    print(f"Jumbotron image: {jumbotron_image}")

    most_imports_question_element = driver.find_element(By.CSS_SELECTOR, "fieldset[class=\"flex flex-col gap-16 w-full lg:max-w-[522px] flex-shrink-0 astro-jipml36k\"]")
    most_imports_questions = most_imports_question_element.find_elements(By.TAG_NAME, "label")
    most_import_ques = []
    for most_imports_question in most_imports_questions:
        most_import_ques.append(most_imports_question.text)
    print(most_import_ques)

    most_imports_answer_element = driver.find_element(By.CSS_SELECTOR, "div[class=\"contents astro-jipml36k\"]")
    most_imports_answers = most_imports_answer_element.find_elements(By.TAG_NAME, "section")
    most_import_ans = []
    for most_imports_answer in most_imports_answers:
        most_import_ans.append(driver.execute_script('return arguments[0].textContent;', most_imports_answer))
    print(most_import_ans)


    faq_question_elements = driver.find_elements(By.CSS_SELECTOR, "summary[class=\"group-[&:not(:first-child)]:pt-8 pb-22 tp-headline-s flex justify-between appearance-none cursor-pointer astro-vqbstbga\"]")
    faq_ques = []
    for faq_question_element in faq_question_elements:
        faq_ques.append(faq_question_element.text)
    print(faq_ques)

    faq_answer_elements = driver.find_elements(By.CSS_SELECTOR, "div[class=\"pb-16 astro-vqbstbga\"]")
    faq_ans = []
    for faq_answer_element in faq_answer_elements:
        faq_ans.append(driver.execute_script('return arguments[0].textContent;', faq_answer_element))
    print(faq_ans)

    json_data = {}
    json_data['meta_title'] = meta_title
    json_data['meta_description'] = meta_description
    json_data['meta_keyword'] = ""
    json_data['url'] = url
    json_data['h1'] = h1
    json_data['jumbotron_text'] = jumbotron_text
    json_data['jumbotron_image'] = jumbotron_image

    most_import_json = []
    index_most = 0
    for _ in range(len(most_import_ans)):
        most_import_json.append({"title": most_import_ques[index_most], "description": most_import_ans[index_most]})
        index_most +=1

    faq_json = []
    index_faq = 0
    for _ in range(len(faq_ans)):
        faq_json.append({"question": faq_ques[index_faq], "answer": faq_ans[index_faq]})
        index_faq +=1

    json_data['most_import'] = most_import_json
    json_data['faq'] = faq_json
    data = {}
    data[f'page{index}'] = json_data


    prettified_json = json.dumps(data, indent=4)
        
    print(prettified_json)

    parsed_url = urlparse(url)
    path = parsed_url.path

    # Extract the desired string
    desired_string = path.split("/")[-2]

    with open(f"json_files/{desired_string}.json", 'w', encoding='utf-8') as file:
        # Write the JSON data to the file
        json.dump(data, file, ensure_ascii=False)

# scrape("https://iproyal.com/other-proxies/4chan-proxy/", 1)