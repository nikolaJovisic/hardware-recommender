import csv
from typing import List

from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as ec


def scrape_amazon_product_titles(search_text: str, filename: str) -> None:
    """ Keep browser open after end of the program

    chrome_options = Options()
    chrome_options.add_experimental_option("detach", True)
    driver = webdriver.Chrome('chromedriver.exe', chrome_options=chrome_options)
    """

    driver = webdriver.Chrome('chromedriver.exe')
    driver.get('https://www.amazon.com/')

    WebDriverWait(driver, 20).until(ec.presence_of_element_located((By.ID, 'twotabsearchtextbox')))
    driver.find_element_by_id('twotabsearchtextbox').send_keys(search_text)
    driver.find_element_by_id('nav-search-submit-button').click()

    elem = driver.find_element_by_xpath("//*[@class='s-pagination-item s-pagination-disabled']")  # number of pages

    product_titles = []
    j = 0
    for i in range(int(elem.text)-1):
        WebDriverWait(driver, 20).until(ec.presence_of_element_located(
            (By.XPATH, "//*[@class='a-size-base a-color-base a-link-normal s-underline-text s-underline-link-text s-link-style']")))

        elem = driver.find_elements_by_xpath("//*[@class='a-size-medium a-color-base a-text-normal']")
        product_titles += [title.text for title in elem]
        for e in elem:
            j += 1
            print(f'{j}. {e.text}\n')

        # driver.get(f'https://amazon.com/s?k=motherboard+cpu+ram&page={i}&crid=Q0X1AU3SVM0O&qid=1670188720&sprefix=%2Caps%2C254&ref=sr_pg_1')
        # driver.find_element_by_xpath("//*[@class='s-pagination-item s-pagination-next s-pagination-button s-pagination-separator']").click()
        WebDriverWait(driver, 20).until(ec.element_to_be_clickable((By.XPATH, "//*[@class='s-pagination-item s-pagination-next s-pagination-button s-pagination-separator']"))).click()

    driver.close()

    save_scraped_data(product_titles, filename)


def save_scraped_data(scraped_data: List[str], filename: str) -> None:
    with open(filename, 'w', encoding='utf8', newline='') as file:
        writer = csv.writer(file, delimiter='\t', lineterminator='\n')
        for data in scraped_data:
            writer.writerow([data])
