from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait
from selenium.common.exceptions import *
from time import sleep
import scraping_bot

options = webdriver.ChromeOptions()
options.add_argument('--headless=new')

driver = webdriver.Chrome(options=options)
driver.maximize_window()
driver.get("https://iproyal.com/other-proxies/")

WebDriverWait(driver, 20).until(EC.element_to_be_clickable((By.CSS_SELECTOR, "button[id=\"CybotCookiebotDialogBodyLevelButtonLevelOptinAllowAll\"]")))
sleep(2)
accept_cookie_button = driver.find_element(By.CSS_SELECTOR, "button[id=\"CybotCookiebotDialogBodyLevelButtonLevelOptinAllowAll\"]")
accept_cookie_button.click()
sleep(2)


urls = []

while(True):
    urls_elements = driver.find_elements(By.CSS_SELECTOR, "a[class=\"group flex items-center gap-4 mt-auto astro-zgb246lv outlined-button\"]")
    for url_element in urls_elements:
        urls.append(url_element.get_attribute('href'))
    try:
        last_page = driver.find_element(By.CSS_SELECTOR, "span[class=\"outlined-button w-full text-size-[14px] px-8 sm:px-16 pagination-link\"]")
        if last_page.text == "Next":
            break
    except:
        pass

    page_buttons = driver.find_elements(By.CSS_SELECTOR, "a[class=\"outlined-button w-full text-size-[14px] px-8 sm:px-16 pagination-link\"]")
    for page_button in page_buttons:
        if page_button.text == "Next":
            # page_button.click()
            driver.execute_script("arguments[0].click();", page_button)
            break
    break
    sleep(4)
driver.quit()
print(len(urls))

index = 1
for url in urls:
    scraping_bot.scrape(url, index)
    index += 1
driver.quit()