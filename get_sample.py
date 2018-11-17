import argparse
import datetime
import json
import logging

from functools import lru_cache
from habanero import Crossref
from multiprocessing import Pool
from pathlib import Path


BASE_URL = 'https://api.crossref.org'
SAMPLE_CHUNK_SIZE = 100
CRAPI_KEY_FN = '.crapi_key'


def crapi_key():
    return load_key(CRAPI_KEY_FN)


@lru_cache(maxsize=None)
def load_key(key):
    with open(Path.home() / key, mode='r') as kf:
        key_value = kf.read()
    return json.loads(key_value)


API_KEY = crapi_key().get('Authorization')
POLITE = crapi_key().get('Mailto')


def get_sample_chunk(size):
    return Crossref(base_url=BASE_URL, mailto=POLITE, api_key=API_KEY) \
        .works(sample=size) \
        .get('message', {}).get('items')


def generate_sample_args(size):
    sample_count = int(size / SAMPLE_CHUNK_SIZE)
    sizes = [SAMPLE_CHUNK_SIZE] * sample_count
    if size % SAMPLE_CHUNK_SIZE != 0:
        sizes.append(size % SAMPLE_CHUNK_SIZE)
    return sizes


def generate_sample_data(size):
    logging.info('Getting a sample of items')
    sample = []
    with Pool() as pool:
        sample = pool.map(get_sample_chunk, generate_sample_args(size))
    sample = [item for sublist in sample for item in sublist]
    return {'timestamp': datetime.datetime.utcnow().replace(
                         tzinfo=datetime.timezone.utc).isoformat(),
            'size': size,
            'sample': sample}


def save_sample_data(sample_data, file_path):
    with open(file_path, 'w+') as file:
        file.write(json.dumps(sample_data, indent=4))
    logging.info('Sample data written to {}'.format(file_path))


if __name__ == '__main__':
    parser = argparse.ArgumentParser(
            description='Draw a sample of items from Crossref collection')
    parser.add_argument('-s', '--size', help='size of sample', type=int,
                        required=True)
    parser.add_argument('-o', '--output', help='output file',
                        type=str, required=True)
    args = parser.parse_args()

    sample_data = generate_sample_data(args.size)
    save_sample_data(sample_data, args.output)
