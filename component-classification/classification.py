import csv
from typing import Dict, List, Tuple

import numpy as np
import matplotlib.pyplot as plt
from collections import Counter

import pandas as pd
from fuzzywuzzy import fuzz
import jellyfish
import difflib


def print_histogram(components: str) -> Dict[str, int]:
    with open(f"../scraper/data/{components}.txt", mode='r', encoding="utf-8") as file:
        reader = csv.reader(file, delimiter='\t', lineterminator='\n')
        dataset = [line[0] for line in reader]

    dataset = ' '.join(dataset).translate({ord(i): ' ' for i in ',()/&'}).lower().split()
    # dataset = ' '.join(dataset).lower().split()

    dataset = [data for data in dataset if data not in ['-', 'up', 'for', 'to', 'pc', 'desktop', 'desk', 'top', 'computer', 'with', 'gaming', 'and']]

    counts = dict(Counter(dataset).most_common(20))

    labels, values = zip(*counts.items())

    ind_sort = np.argsort(values)[::-1]

    labels = np.array(labels)[ind_sort]
    values = np.array(values)[ind_sort]

    indexes = np.arange(len(labels))

    plt.bar(indexes, values)

    plt.xticks(indexes, labels)
    plt.title(components)
    plt.show()

    return dict(Counter(dataset))
    # return counts


def check_configurations(cpus: Dict[str, int], ram: Dict[str, int], motherboards: Dict[str, int]) -> None:
    with open(f"../scraper/data/combined_configurations.txt", mode='r', encoding="utf-8") as file:
        reader = csv.reader(file, delimiter='\t', lineterminator='\n')
        dataset = [line[0] for line in reader]

    dataset = [s.translate({ord(i): ' ' for i in ',()/&'}).lower() for s in dataset]

    dataset_modified = []
    for data in dataset:
        dataset_modified.append(' '.join([d for d in data.split() if d not in ['-', 'up', 'for', 'to', 'pc', 'desktop', 'desk', 'top', 'computer', 'with', 'gaming', 'and']]))

    # dataset = ['msi performance gaming amd ryzen 2nd and 3rd gen am4 m.2 usb 3 ddr4 dvi hdmi crossfire atx motherboard b450 gaming plus max']

    df = pd.DataFrame(columns=['CPUs', 'RAM', 'Motherboards'])

    print('cpu')
    process_data(dataset_modified, cpus, 'CPUs', df)
    print('ram')
    process_data(dataset_modified, ram, 'RAM', df)
    print('motherboard')
    process_data(dataset_modified, motherboards, 'Motherboards', df)

    df.to_csv('data/extracted_components.csv', index=False)


def process_data(dataset: List[str], components: Dict[str, int], component_name: str, df: pd.DataFrame) -> None:
    configs = get_component_occurrences(dataset, components)

    extracted_strings = []
    for i, config in enumerate(configs):
        # labels, values = zip(*config.items())
        labels, values = [], []
        for c in config:
            labels.append(c[0])
            values.append(c[1])

        values = [v if v >= max(values)/20 else 0 for v in values]

        separated_values = separate_values(values)
        extracted_component, extracted_component_index, extracted_component_value = extract_component(values, separated_values)

        extracted_string = extract_string(extracted_component, extracted_component_index, extracted_component_value,
                                          separated_values, values, labels)
        extracted_strings.append(extracted_string)

        labels = np.array(labels)
        values = np.array(values)

        indexes = np.arange(len(labels))

        plt.bar(indexes, values)

        plt.xticks(indexes, labels)
        plt.title(component_name)
        plt.show()

    df[component_name] = extracted_strings


def get_component_occurrences(dataset: List[str], components: Dict[str, int]) -> List[List[Tuple[str, int]]]:
    configs = []
    for data in dataset:
        config = []
        """for string in data.split():
            config[string] = 0"""
        for string in data.split():
            """ ---first approach
            try:
                config.append([string, components[max(components.keys(), key=lambda i: difflib.SequenceMatcher(None, i, string).ratio())]])
            except:
                config.append([string, 0])
                
            ---second approach    
            sum = 0
            for component in components.keys():
                if jellyfish.jaro_distance(component, string) >= 0.9:
                    # config[string] += components[component]
                    sum += components[component]
            config.append([string, sum])
            """
            try:
                config.append((string, components[string]))
            except:
                config.append((string, 0))
        configs.append(config)
        # if len(configs) > 10:
        # break
    return configs


def separate_values(values: List[int]) -> List[Tuple[int, int]]:
    values.append(0)
    separated_values = []
    in_sequence = 0
    for i, value in enumerate(values):
        if in_sequence != 0 and value == 0:
            separated_values.append((i-in_sequence, in_sequence))
            in_sequence = 0
        elif value != 0:
            in_sequence += 1
    values.pop(len(values)-1)

    return separated_values


def extract_component(values: List[int], separated_values: List[Tuple[int, int]]) -> Tuple[Tuple[int, int], int, int]:
    max_index = 0
    max_value = 0
    for i, separated_value in enumerate(separated_values):
        if sum(values[separated_value[0]:separated_value[0]+separated_value[1]]) > max_value:
            max_value = sum(values[separated_value[0]:separated_value[0]+separated_value[1]])
            max_index = i

    return separated_values[max_index], max_index, max_value


def extract_string(extracted_component: Tuple[int, int], extracted_component_index: int, extracted_component_value: int, separated_values: List[Tuple[int, int]],
                   values: List[int], labels: List[str]) -> str:
    sum_of_next, sum_of_prev = 0, 0
    if extracted_component_index < len(separated_values) - 1:
        sum_of_next = sum(values[separated_values[extracted_component_index + 1][0]:
                                 separated_values[extracted_component_index + 1][0] +
                                 separated_values[extracted_component_index + 1][1]])
    if extracted_component_index > 0:
        sum_of_prev = sum(values[separated_values[extracted_component_index - 1][0]:
                                 separated_values[extracted_component_index - 1][0] +
                                 separated_values[extracted_component_index - 1][1]])
    if sum_of_next >= extracted_component_value / 2 and sum_of_next > sum_of_prev and \
            separated_values[extracted_component_index + 1][0] - (extracted_component[0] + extracted_component[1]) == 1:
        extracted_component = (
        extracted_component[0], extracted_component[1] + separated_values[extracted_component_index + 1][1] + 1)
    elif sum_of_prev >= extracted_component_value / 2 and extracted_component[0] - (
            separated_values[extracted_component_index - 1][0] + separated_values[extracted_component_index - 1][
        1]) == 1:
        extracted_component = (separated_values[extracted_component_index - 1][0],
                               extracted_component[1] + separated_values[extracted_component_index - 1][1] + 1)
    extracted_string = ' '.join(labels[extracted_component[0]:extracted_component[0] + extracted_component[1]])
    return extracted_string


if __name__ == '__main__':
    cpus = print_histogram('processors')
    ram = print_histogram('ram')
    motherboards = print_histogram('motherboards')

    check_configurations(cpus, ram, motherboards)

    """ ---Similarity metrics comparison
    print(fuzz.ratio('Intel Core i9 - 12900K', 'Intel Core i7 - 12700KF'))
    print(difflib.SequenceMatcher(None, 'Intel Core i9 - 12900K', 'Intel Core i7 - 12700KF').ratio())
    print(jellyfish.jaro_distance('Intel Core i9 - 12900K', 'Intel Core i7 - 12700KF'))
    """
