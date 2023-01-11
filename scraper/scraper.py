import csv
from typing import List

from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as ec


def scrape_amazon_product_titles(search_text: str, filename: str, department: str = '', limit: int = 0) -> None:
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

    if department != '':
        spans = driver.find_elements_by_xpath('.//span[@class = "a-size-base a-color-base"]')
        for span in spans:
            if span.text == department:
                span.click()
                break

    page_number = int(driver.find_element_by_xpath("//*[@class='s-pagination-item s-pagination-disabled']").text)
    if limit == 0 or limit > page_number:
        limit = page_number

    product_titles = []
    j = 0
    for i in range(limit-1):
        WebDriverWait(driver, 20).until(ec.presence_of_element_located(
            (By.XPATH, "//*[@class='a-size-base a-color-base a-link-normal s-underline-text s-underline-link-text s-link-style']")))

        sponsored_products = get_sponsored_products(driver)
        elem = driver.find_elements_by_xpath("//*[@class='a-size-medium a-color-base a-text-normal']")
        current_titles = [title.text for title in elem]
        current_titles = [title for title in current_titles if title not in sponsored_products]

        product_titles += current_titles
        for title in current_titles:
            j += 1
            print(f'{j}. {title}\n')

        WebDriverWait(driver, 20).until(ec.element_to_be_clickable((By.XPATH, "//*[@class='s-pagination-item s-pagination-next s-pagination-button s-pagination-separator']"))).click()

    driver.close()

    save_data(product_titles, filename)


def get_sponsored_products(driver: webdriver.Chrome) -> List[str]:
    sponsored_spans = driver.find_elements_by_xpath("//*[@class='aok-inline-block s-sponsored-label-info-icon']/parent::a/parent::span/parent::div/following-sibling::h2")
    return [span.text for span in sponsored_spans]


def save_data(scraped_data: List[str], filename: str) -> None:
    with open(filename, 'w', encoding='utf8', newline='') as file:
        writer = csv.writer(file, delimiter='\t', lineterminator='\n')
        for data in scraped_data:
            writer.writerow([data])


def combine_data(destination_file: str, files: List[str]) -> None:
    titles = []
    for f in files:
        with open(f, 'r', encoding='utf8') as file:
            reader = csv.reader(file, delimiter='\t', lineterminator='\n')
            titles += [line[0] for line in reader]

    titles = list(set(titles))
    titles = [title for title in titles if len(title.split(' ')) >= 20]
    save_data(titles, destination_file)


if __name__ == '__main__':
    # scrape_amazon_product_titles('cpu', 'data/processors.txt', department='Computer CPU Processors', limit=100)
    # scrape_amazon_product_titles(search_text='ram', filename='data/ram.txt', department='Computer Memory', limit=100)
    # scrape_amazon_product_titles(search_text='motherboard', filename='data/motherboards.txt', department='Computer Motherboards', limit=100)
    # scrape_amazon_product_titles(search_text='computer', filename='data/tower_computers.txt', department='Tower Computers', limit=100)
    # scrape_amazon_product_titles(search_text='computer', filename='data/traditional_laptops.txt', department='Traditional Laptop Computers', limit=100)
    # scrape_amazon_product_titles(search_text='computer', filename='data/all_in_one_computers.txt', department='All-in-One Computers', limit=100)
    # scrape_amazon_product_titles(search_text='computer', filename='data/mini_computers.txt', department='Mini Computers', limit=100)

    files = ['data/tower_computers.txt', 'data/traditional_laptops.txt', 'data/all_in_one_computers.txt',
             'data/mini_computers.txt']
    combine_data(destination_file='data/computers.txt', files=files)
