import json
import pandas as pd
import re

from config import MIN_REF_LEN, REGEX_MONTH_REMOVE, REGEX_RANDOM_REMOVE, \
    REGEX_REMOVE, STYLES
from random import random


def read_ref_strings_data(path):
    dataset = []
    for style in STYLES:
        with open(path + '/dataset-' + style + '.json', 'r') as file:
            data = json.loads(file.read())
        dataset.extend([(d['target_gt']['DOI'], d['ref_string'], style)
                        for d in data['dataset']])
    return pd.DataFrame(dataset, columns=['doi', 'string', 'style'])


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
