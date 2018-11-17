import argparse
import logging
import pandas as pd
import pickle

from config import N_FEATURES, NGRAM_RANGE
from dataset import add_noise, clean_data, read_ref_strings_data, \
    remove_technical_parts, rearrange_tokens, generate_unknown
from features import get_features, select_features_chi2
from random import seed
from sklearn.linear_model import LogisticRegression


def clean(dataset, random_state=0):
    seed(random_state)
    dataset = clean_data(dataset)
    dataset['string'] = dataset['string'].apply(remove_technical_parts)
    dataset['string'] = dataset['string'].apply(add_noise)
    return dataset


def train(dataset, random_state=0):
    count_vectorizer, tfidf_transformer, features = \
        get_features(dataset['string'], nfeatures=N_FEATURES,
                     feature_selector=select_features_chi2, ngrams=NGRAM_RANGE)
    model = LogisticRegression(random_state=random_state).fit(features,
                                                              dataset['style'])
    return count_vectorizer, tfidf_transformer, model


def save(path, count_vectorizer, tfidf_transformer, model):
    with open(args.output, 'wb') as file:
        pickle.dump((count_vectorizer, tfidf_transformer, model), file)


if __name__ == '__main__':
    parser = argparse.ArgumentParser(
            description='Train a citation style classifier')
    parser.add_argument('-d', '--dataset', help='dataset directory path',
                        type=str, required=True)
    parser.add_argument('-u', '--unknown',
                        help='number of strings of "unknown" style', type=int)
    parser.add_argument('-o', '--output', help='output model file', type=str,
                        required=True)
    parser.add_argument('-r', '--randomstate', help='seed', type=int,
                        default=0)
    args = parser.parse_args()

    logging.basicConfig(level=logging.INFO,
                        format='%(asctime)s %(levelname)s %(message)s')

    logging.info('Reading the data...')
    dataset = read_ref_strings_data(args.dataset)
    logging.info('Dataset size: {}'.format(dataset.shape[0]))

    logging.info('Cleaning the data...')
    dataset = clean(dataset, random_state=args.randomstate)
    logging.info('Dataset size after cleaning: {}'.format(dataset.shape[0]))

    if args.unknown is not None and args.unknown > 0:
        logging.info('Adding "unknown" strings...')
        dataset_unknown = generate_unknown(dataset, args.unknown,
                                           random_state=args.randomstate)
        dataset = pd.concat([dataset, dataset_unknown])
        logging.info('Dataset size after adding strings of unknown style: {}'
                     .format(dataset.shape[0]))

    logging.info('Training...')
    count_vectorizer, tfidf_transformer, model = \
        train(dataset, random_state=args.randomstate)

    save(args.output, count_vectorizer, tfidf_transformer, model)
    logging.info('Model written to {}'.format(args.output))
