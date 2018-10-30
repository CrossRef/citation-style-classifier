import numpy as np
import re
import scipy.sparse as sp

from config import NGRAM_RANGE, REGEX_WORD_TO_TOKEN
from sklearn.ensemble import RandomForestClassifier
from sklearn.feature_extraction.text import CountVectorizer, TfidfTransformer
from sklearn.feature_selection import chi2


def tokens_to_classes(s):
    for r, t in REGEX_WORD_TO_TOKEN.items():
        s = re.sub(r, ' ' + t + ' ', s)
    s = 'start ' + s + 'end'
    s = re.sub(' +', ' ', s).strip()
    return s


def select_features_rf(tfidf, response, feature_names, nfeatures):
    rf = RandomForestClassifier(n_estimators=200, max_depth=3, random_state=5)
    rf_model = rf.fit(tfidf, response)
    feature_importances = np.argsort(rf_model.feature_importances_)
    feature_names = np.array(feature_names)
    feature_names = feature_names[feature_importances]
    return feature_names[-nfeatures:]


def select_features_chi2(tfidf, response, feature_names, nfeatures):
    feature_names_sorted = []
    for label in list(set(response)):
        features_chi2 = chi2(tfidf, response == label)[0]
        indices = np.argsort(features_chi2)
        fns = np.array(feature_names)
        fns = fns[indices][::-1]
        feature_names_sorted.append(fns)
    feature_names = set()
    for i in range(nfeatures):
        if len(feature_names) == nfeatures:
            break
        nf = [x[i] for x in feature_names_sorted]
        for n in nf:
            if len(feature_names) == nfeatures:
                break
            feature_names.add(n)
    return feature_names


def get_tfidf_features(strings, response=None, count_vectorizer=None,
                       tfidf_transformer=None, nfeatures=None,
                       ngrams=NGRAM_RANGE, feature_selector=None):
    if count_vectorizer is None:
        # fit and calculate features (train set mode)
        freq_nfeatures = None
        if feature_selector is None:
            freq_nfeatures = nfeatures
        count_vectorizer = CountVectorizer(preprocessor=tokens_to_classes,
                                           max_features=freq_nfeatures,
                                           ngram_range=ngrams)
        counts = count_vectorizer.fit_transform(strings)
        tfidf_transformer = TfidfTransformer()
        tfidf = tfidf_transformer.fit_transform(counts)
        if feature_selector is not None and nfeatures is not None \
                and response is not None:
            # feature selection
            feature_names = \
                feature_selector(tfidf, response,
                                 count_vectorizer.get_feature_names(),
                                 nfeatures)
            count_vectorizer = CountVectorizer(preprocessor=tokens_to_classes,
                                               ngram_range=ngrams,
                                               vocabulary=feature_names)
            counts = count_vectorizer.fit_transform(strings)
            tfidf_transformer = TfidfTransformer()
            tfidf = tfidf_transformer.fit_transform(counts)
    else:
        # calculate features (test set mode)
        counts = count_vectorizer.transform(strings)
        tfidf = tfidf_transformer.transform(counts)
    return count_vectorizer, tfidf_transformer, tfidf


def get_features(strings, response=None, count_vectorizer=None,
                 tfidf_transformer=None, nfeatures=None,
                 ngrams=NGRAM_RANGE, feature_selector=None):
    count_vectorizer, tfidf_transformer, features = \
        get_tfidf_features(strings, response=response, nfeatures=nfeatures,
                           count_vectorizer=count_vectorizer,
                           tfidf_transformer=tfidf_transformer,
                           ngrams=ngrams, feature_selector=feature_selector)
    lengths = [[len(s)] for s in strings]
    features = sp.hstack((features, sp.csr_matrix(lengths)))

    return count_vectorizer, tfidf_transformer, features
