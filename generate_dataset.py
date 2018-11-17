import argparse
import csv
import json
import logging
import re
import requests

from multiprocessing import Pool


CN_BASE_URL = 'http://data.crossref.org'


def remote_call(uri, headers={}):
    r = requests.get(uri, headers=headers)
    r.encoding = 'UTF-8'
    code = r.status_code
    return code, str(r.text)


def format_ref_string(item, style):
    doi = item.get('DOI')
    headers = {'Accept': 'text/x-bibliography; style={}'.format(style)}
    code, ref_string = remote_call('{}/{}'.format(CN_BASE_URL, doi), headers)
    if code != 200:
        logging.error(
            'Creating ref string in style {} for DOI {} failed with code {}'.
            format(style, doi, code))
        return None
    for rem in ['doi\:10\..*',
                'Available at: http://dx.doi.org/.*',
                'Crossref. Web.',
                '[^ ]*doi\.org/10\.[^ ]*',
                '[^ ]*' + doi[:5] + '[^ ]*']:
        ref_string = re.sub(rem, '', ref_string)
    ref_string = re.sub('\n', ' ', ref_string)
    ref_string = re.sub(' +', ' ', ref_string)
    return ref_string.strip()


def generate_dataset(sample, style):
    logging.info('Generating dataset')
    with Pool() as p:
        results = p.starmap(format_ref_string, [(s, style) for s in sample])
    return [(s.get('DOI'), r) for s, r in zip(sample, results)]


if __name__ == '__main__':
    parser = argparse.ArgumentParser(
            description='create an evaluation dataset')
    parser.add_argument('-l', '--style', help='citation style name',
                        type=str, default='apa')
    parser.add_argument('-s', '--sample', help='input sample file',
                        type=str, required=True)
    parser.add_argument('-o', '--output', help='output dataset file',
                        type=str, required=True)
    args = parser.parse_args()

    with open(args.sample, 'r') as file:
        sample_data = json.loads(file.read())
    dataset = generate_dataset(sample_data.get('sample'), args.style)

    with open(args.output, 'w') as csvfile:
        writer = csv.writer(csvfile)
        for doi, ref_string in dataset:
            writer.writerow([doi, args.style, ref_string])
