import collections
import csv
from fuzzywuzzy import fuzz

from scraper import scrape_amazon_product_titles
from scraper import save_scraped_data


def combine_data() -> None:
    with open('data/configurations1.txt', 'r', encoding='utf8') as file:
        reader = csv.reader(file, delimiter='\t', lineterminator='\n')
        titles = [line[0] for line in reader]

    with open('data/configurations2.txt', 'r', encoding='utf8') as file:
        reader = csv.reader(file, delimiter='\t', lineterminator='\n')
        titles += [line[0] for line in reader]

    titles = list(set(titles))
    save_scraped_data(titles, 'data/combined_configurations.txt')


if __name__ == '__main__':
    # scrape_amazon_product_titles('motherboard cpu ram', 'data/configurations1.txt')
    # scrape_amazon_product_titles('motherboard', 'data/motherboards.txt')
    # scrape_amazon_product_titles('processor', 'data/processors.txt')
    # scrape_amazon_product_titles('ram', 'data/ram.txt')
    # scrape_amazon_product_titles('motherboard configurations', 'data/configurations2.txt')
    # combine_data()
    print()
