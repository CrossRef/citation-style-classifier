import argparse
import pickle

from features import get_features


if __name__ == '__main__':
    parser = argparse.ArgumentParser(
            description='Infer citation style based on the reference string')
    parser.add_argument('-m', '--model', help='model file', type=str,
                        default='models/default-model')
    parser.add_argument('-r', '--reference', help='reference string',
                        type=str)
    parser.add_argument('-i', '--input', help='file with reference strings',
                        type=str)
    parser.add_argument('-o', '--output', help='output file', type=str)
    args = parser.parse_args()

    with open(args.model, 'rb') as file:
        model = pickle.load(file)
    count_vectorizer, tfidf_transformer, model = tuple(model)

    if args.reference:
        _, _, features = get_features([args.reference],
                                      count_vectorizer=count_vectorizer,
                                      tfidf_transformer=tfidf_transformer)
        print(model.predict(features)[0])

    if args.input:
        with open(args.input, 'r') as file:
            ref_strings = [line.strip() for line in file]
        _, _, features = get_features(ref_strings,
                                      count_vectorizer=count_vectorizer,
                                      tfidf_transformer=tfidf_transformer)
        styles = model.predict(features)
        with open(args.output, 'w') as file:
            file.writelines([s + '\n' for s in styles])
