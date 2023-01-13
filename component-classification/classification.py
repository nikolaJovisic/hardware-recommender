import csv
import re
from typing import Dict, List, Tuple

import numpy as np
import matplotlib.pyplot as plt
from collections import Counter

import pandas as pd
from pandas import Series
from sklearn import preprocessing
from fuzzywuzzy import fuzz
import jellyfish
import difflib


def print_histogram(components: str) -> Dict[str, int]:
    with open(f"../scraper/data/{components}.txt", mode='r', encoding="utf-8") as file:
        reader = csv.reader(file, delimiter='\t', lineterminator='\n')
        dataset = [line[0] for line in reader]

    dataset = ' '.join(dataset).translate({ord(i): ' ' for i in ',()/&|@\'\"'}).lower().split()
    # dataset = ' '.join(dataset).lower().split()

    dataset = [data for data in dataset if data not in ['-', 'up', 'for', 'to', 'pc', 'desktop', 'desk', 'top',
                                                        'computer', 'with', 'gaming', 'and', 'mini', 'laptop', 'renewed']]

    counts = dict(Counter(dataset).most_common(20))

    # labels, values = zip(*counts.items())
    #
    # ind_sort = np.argsort(values)[::-1]
    #
    # labels = np.array(labels)[ind_sort]
    # values = np.array(values)[ind_sort]
    #
    # values = preprocessing.normalize([values])
    # values = values[0]
    #
    # indexes = np.arange(len(labels))
    #
    # plt.bar(indexes, values)
    #
    # plt.xticks(indexes, labels)
    # plt.title(components)
    # plt.show()

    return dict(Counter(dataset))
    # return counts


def check_configurations(cpus: Dict[str, int], ram: Dict[str, int], motherboards: Dict[str, int]) -> pd.DataFrame:
    with open(f"../scraper/data/computers.txt", mode='r', encoding="utf-8") as file:
        reader = csv.reader(file, delimiter='\t', lineterminator='\n')
        dataset = [line[0] for line in reader]

    dataset = [s.translate({ord(i): ' ' for i in ',()/&|@\'\"'}).lower() for s in dataset]

    dataset_modified = []
    for data in dataset:
        dataset_modified.append(' '.join([d for d in data.split() if d not in ['-', 'up', 'for', 'to', 'pc', 'desktop',
                                'desk', 'top', 'computer', 'with', 'gaming', 'and', 'mini', 'laptop', 'renewed']]))

    df = pd.DataFrame(columns=['CPUs', 'RAM', 'Motherboards'])

    print('cpu')
    process_data(dataset_modified, cpus, 'CPUs', df)
    print('ram')
    process_data(dataset_modified, ram, 'RAM', df)
    print('motherboard')
    process_data(dataset_modified, motherboards, 'Motherboards', df)

    df = cleanup_data(df)

    df.to_csv('data/extracted_components.csv', index=False)
    df[['CPUs', 'RAM']].to_csv('data/extracted_components_minimized.csv', index=False)

    return df[['CPUs', 'RAM']]


def cleanup_data(df: pd.DataFrame) -> pd.DataFrame:
    regex_cpu = '[0-9]{4,}[A-Za-z]+|i[0-9]-[0-9A-Za-z]+|[A-Za-z][0-9]{4,}|i[0-9]|ryzen [0-9]'

    df = df.loc[df['RAM'].str.contains(pat='ddr', regex=True)]
    df = df.loc[df['RAM'].str.contains(pat='[0-9]{0,2}gb', regex=True)]
    df = df.loc[df['CPUs'].str.contains(pat='intel|amd|ryzen', regex=True)]
    df = df.loc[df['CPUs'].str.contains(pat=regex_cpu, regex=True)]
    df = df.drop_duplicates()

    for _, row in df.iterrows():
        row['CPUs'] = ' '.join([s for s in row['CPUs'].split() if re.search('ddr|gb|mhz|ram|ssd|1080p|[0-9]{4}x[0-9]{3,4}', s) is None])
        row['RAM'] = ' '.join([s for s in row['RAM'].split() if re.search('gddr', s) is None])
        remove_noise_ram(row)
    return df


def remove_noise_ram(row: Series) -> None:
    start, end = re.search('ddr', row['RAM']).regs[0]
    split_row = row['RAM'].split()
    len_sum = 0
    position = 0
    for i, s in enumerate(split_row):
        if len_sum == start:
            position = i
            break
        len_sum += len(s) + 1
    if position > 0 and re.search('gb', split_row[position - 1]):
        split_row = [s for i, s in enumerate(split_row) if re.search('gb', s) is None or i in [position - 1, position]]
    row['RAM'] = ' '.join(split_row)


def process_data(dataset: List[str], components: Dict[str, int], component_name: str, df: pd.DataFrame) -> None:
    configs = get_component_occurrences(dataset, components)

    extracted_strings = []
    for i, config in enumerate(configs):
        labels, values = [], []
        for c in config:
            labels.append(c[0])
            values.append(c[1])

        regex_cpu = '[0-9]{4,}[A-Za-z]+|i[0-9]-[0-9A-Za-z]+|[A-Za-z][0-9]{4,}|i[0-9]'
        if component_name == 'CPUs':
            values = [max(values)/2 if re.search(regex_cpu, labels[i]) else v for i, v in enumerate(values)]

        values = [v if v >= max(values)/20 else 0 for v in values]

        separated_values = separate_values(values)
        extracted_component, extracted_component_index, extracted_component_value = extract_component(values, separated_values)

        extracted_string = extract_string(extracted_component, extracted_component_index, extracted_component_value,
                                          separated_values, values, labels)
        extracted_strings.append(extracted_string)

        # labels = np.array(labels)
        # values = np.array(values)
        #
        # indexes = np.arange(len(labels))
        #
        # plt.bar(indexes, values)
        #
        # plt.xticks(indexes, labels)
        # plt.title(component_name)
        # plt.show()

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
        #     break
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


def add_motherboards(dataframe: pd.DataFrame):
    with open(f"../scraper/data/motherboards.txt", mode='r', encoding="utf-8") as file:
        reader = csv.reader(file, delimiter='\t', lineterminator='\n')
        motherboard_dataset = [line[0] for line in reader]

    motherboard_dataset = [s.translate({ord(i): ' ' for i in ',()/&|@\'\"'}).lower() for s in motherboard_dataset]

    data = []
    i = 0
    for _, row in dataframe.iterrows():
        i += 1
        print(i)
        for motherboard in motherboard_dataset:
            d = []
            cpu_regex = ''
            ram_regex = ''

            if re.search(' i-?[357]', row['CPUs']):
                d.append(row['CPUs'])
                cpu_regex = ' i-?[357]'
            elif re.search(' i-?9', row['CPUs']):
                d.append(row['CPUs'])
                cpu_regex = ' i-?9'
            elif re.search('ryzen 3', row['CPUs']):
                d.append(row['CPUs'])
                cpu_regex = 'ryzen 3'
            elif re.search('ryzen [579]', row['CPUs']):
                d.append(row['CPUs'])
                cpu_regex = 'ryzen [579]'

            if re.search('ddr3', row['RAM']):
                d.append(row['RAM'])
                ram_regex = 'ddr3'
            elif re.search('ddr4', row['RAM']):
                d.append(row['RAM'])
                ram_regex = 'ddr4'
            elif re.search('ddr5', row['RAM']):
                d.append(row['RAM'])
                ram_regex = 'ddr5'

            if cpu_regex != '' and ram_regex != '':
                if re.search(cpu_regex, motherboard) and re.search(ram_regex, motherboard):
                    d.append(' '.join(motherboard.split()[:4]))
                    if re.search(' i-?[3579]|ryzen [3579]', d[2]) is None:
                        data.append(d)

    final_dataframe = pd.DataFrame(data=data, columns=['CPU', 'RAM', 'Motherboard'])
    final_dataframe.drop_duplicates(inplace=True)
    final_dataframe.to_csv('data/extracted_components.csv', index=False)


if __name__ == '__main__':
    cpus = print_histogram('processors')
    ram = print_histogram('ram')
    motherboards = print_histogram('motherboards')

    dataframe = check_configurations(cpus, ram, motherboards)

    add_motherboards(dataframe)

    """ ---Similarity metrics comparison
    print(fuzz.ratio('Intel Core i9 - 12900K', 'Intel Core i7 - 12700KF'))
    print(difflib.SequenceMatcher(None, 'Intel Core i9 - 12900K', 'Intel Core i7 - 12700KF').ratio())
    print(jellyfish.jaro_distance('Intel Core i9 - 12900K', 'Intel Core i7 - 12700KF'))
    """
