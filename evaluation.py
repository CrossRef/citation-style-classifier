import pandas as pd

from config import NGRAM_RANGE
from features import get_tfidf_features
from sklearn.metrics import accuracy_score
from sklearn.model_selection import KFold


def evaluate_cv(data, algorithm, folds=5, feature_fun=get_tfidf_features,
                nfeatures=None, ngrams=NGRAM_RANGE, feature_selector=None,
                random_state=0):
    fold_data = KFold(n_splits=folds, shuffle=True, random_state=random_state)
    accuracies = []
    cv_data = []
    dois = data['doi'].drop_duplicates()
    for train_index, test_index in fold_data.split(dois):
        # calculate train and test for the current fold
        train_data = data.loc[data['doi'].isin(dois[train_index])]
        test_data = data.loc[data['doi'].isin(dois[test_index])]
        # learn features and IDFs from the fold train and calculate train
        # feature matrix
        count_vectorizer, tfidf_transformer, train_features = \
            feature_fun(train_data['string'], response=train_data['style'],
                        nfeatures=nfeatures, ngrams=ngrams,
                        feature_selector=feature_selector)
        # calculate test feature matrix
        _, _, test_features = feature_fun(test_data['string'],
                                          count_vectorizer=count_vectorizer,
                                          tfidf_transformer=tfidf_transformer)
        # train the main prediction algorithm
        model = algorithm.fit(train_features, train_data['style'])
        # predict styles of the test set
        prediction = model.predict(test_features)
        # update the return data
        accuracies.append(accuracy_score(test_data['style'], prediction))
        cv_data.extend(list(zip(test_data['doi'], test_data['string'],
                                test_data['style'], prediction)))
    return accuracies, \
        pd.DataFrame(cv_data,
                     columns=['doi', 'string', 'style_true', 'style_pred'])
