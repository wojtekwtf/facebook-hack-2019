import numpy as np
import pandas as pd
import tensorflow.keras.backend as K

from deep_person.model import get_corpus_word2vec
from  deep_person.model import get_tokenized_corpus

train_size = 7000
test_size  = 2500

vector_size = 512 # FIXME: must be the same as in "model.py"

COLUMNS = ["cEXT", "cNEU", "cAGR", "cCON", "cOPN"]

def only_visible(row: object):
    return str(row["TEXT"].encode('ascii',errors='ignore'))

def dataset_mypersonality():
    df = pd.read_csv("data/mypersonality_final.csv",
            sep=",", encoding='cp1252')
    df = df.drop(
        ["sEXT", "sNEU", "sAGR", "sCON", "sOPN"] +
        ["#AUTHID", "DATE", "NETWORKSIZE", "BETWEENNESS",
         "NBETWEENNESS","DENSITY","BROKERAGE",
         "NBROKERAGE","TRANSITIVITY"], 1)
    df = df.rename(columns={'STATUS': 'TEXT'})
    df['TEXT'] = df.apply(only_visible, axis=1)
    for col in COLUMNS:
        df[col] = df[col].map(dict(y=1, n=0))
    print(df.head())
    return df

# FIXME: data/* into one big dataset (+ frames -> max_length)
#        framing + essays()  --> max_length (from 20 -> 30)
def dataset_combined():
    pass

def get_labels(df:object, trait:str):
    if trait in COLUMNS:
        return df[trait].values
    return labels

def get_vec4tok(df:object):
    """--- Universal function! ---"""
    corpus = df["TEXT"].values
    print('\tcorpus size: {}'.format(len(corpus)))
    tokenized_corpus = get_tokenized_corpus(corpus)
    word2vec = get_corpus_word2vec(tokenized_corpus)
    X_vecs = word2vec.wv; del word2vec; del corpus
    return X_vecs, tokenized_corpus

def get_training_data(dataset, trait:str):
    X_vecs, tokenized_corpus = get_vec4tok(dataset)
    labels = get_labels(dataset, trait)

    avg_length = 0.0; max_length = 0

    for line in tokenized_corpus:
        if len(line) > max_length:
            max_length = len(line)
        avg_length += float(len(line))

    print('\taverage line length: {}'.format(avg_length /
        float(len(tokenized_corpus))))
    print('\tmax line length: {}'.format(max_length))

    max_text_length = 20

    indexes = set(np.random.choice(len(tokenized_corpus),
        train_size + test_size, replace=False))

    X_train = np.zeros((train_size, max_text_length, vector_size),
            dtype=K.floatx())
    Y_train = np.zeros((train_size, 2), dtype=np.int32)
    X_test = np.zeros((test_size, max_text_length, vector_size),
            dtype=K.floatx())
    Y_test = np.zeros((test_size, 2), dtype=np.int32)

    for i, index in enumerate(indexes):
        for t, token in enumerate(tokenized_corpus[index]):
            if t >= max_text_length:
                break
            if token not in X_vecs:
                continue
            if i < train_size:
                X_train[i, t, :] = X_vecs[token]
            else:
                X_test[i - train_size, t, :] = X_vecs[token]
        if i < train_size:
            Y_train[i, :] = [1.0, 0.0] \
                if labels[index] == 0 else [0.0, 1.0]
        else:
            Y_test[i - train_size, :] = [1.0, 0.0] \
                if labels[index] == 0 else [0.0, 1.0]

    return X_train, Y_train, X_test, Y_test
