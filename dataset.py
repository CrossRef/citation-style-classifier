import csv
import pandas as pd
import re

from config import MIN_REF_LEN, REGEX_MONTH_REMOVE, REGEX_RANDOM_REMOVE, \
    REGEX_REMOVE, STYLES
from random import random, randint


def read_ref_strings_data(path):
    dataset = []
    for style in STYLES:
        with open(path + '/dataset-' + style + '.csv', 'r') as csvfile:
            reader = csv.reader(csvfile)
            for row in reader:
                dataset.append(row)
    return pd.DataFrame(dataset, columns=['doi', 'style', 'string'])


def clean_data(dataset):
    dataset = dataset[pd.notnull(dataset['string'])]
    return dataset[dataset.apply(lambda x: len(x['string']) >= MIN_REF_LEN,
                                 axis=1)]


def remove_technical_parts(s):
    for r in REGEX_REMOVE:
        s = re.sub(r, '', s.strip())
    return s


def add_noise(s):
    for r, e in REGEX_MONTH_REMOVE.items():
        if re.search(r, s) and random() < 0.75:
            s = re.sub(r, e, s).strip()
    for r in REGEX_RANDOM_REMOVE:
        if random() < 0.5:
            s = re.sub(r, '', s).strip()
    return s


def rearrange_tokens(s):
    parts = s.split(' ')
    for _ in range(randint(10, 20)):
        i1, i2 = randint(0, len(parts)-1), randint(0, len(parts)-1)
        parts[i1], parts[i2] = parts[i2], parts[i1]
    return ' '.join(parts)


def generate_unknown(dataset, n, random_state=0):
    dataset_unknown = dataset.sample(n, random_state=random_state)
    dataset_unknown['string'] = \
        dataset_unknown['string'].apply(rearrange_tokens)
    dataset_unknown['style'] = 'unknown'
    return dataset_unknown
