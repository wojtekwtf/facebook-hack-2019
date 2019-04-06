import hashlib, random
def hash_md5(data:object, sample_seed:int=123456):
    # FIXME: use numpy or something faster
    random.seed(sample_seed); sample_data = random.sample(data, 30)
    return hashlib.md5(repr(sample_data).encode('utf-8')).hexdigest()

import os.path, multiprocessing
from gensim.models.word2vec import Word2Vec

model_word2vec = 'deep_person/model/word2vec'

def get_corpus_word2vec(tokenized_corpus:list,
        window_size:int=10, vector_size:int=512):
    dhash = hash_md5(list(tokenized_corpus))
    dfile = model_word2vec+"-"+dhash+".bin"
    if os.path.isfile(dfile):
        print("[WORD2VEC] loading from file (dhash={})".format(dhash))
        return Word2Vec.load(dfile)
    print("[WORD2VEC] generating (dhash={})...".format(dhash))
    word2vec = Word2Vec(sentences=tokenized_corpus,
                        size=vector_size,
                        window=window_size,
                        negative=20,
                        iter=50,
                        seed=1000,
                        workers=multiprocessing.cpu_count())
    word2vec.save(dfile)
    return word2vec

import numpy as np
from nltk.stem.lancaster import LancasterStemmer
from nltk.tokenize import RegexpTokenizer
import tensorflow.keras.backend as K

__tkr = RegexpTokenizer('[a-zA-Z0-9@]+')
__stemmer = LancasterStemmer()

model_tokenized_corpus = 'deep_person/model/tokenized_corpus'

def __nltk_tokens(text:str):
    return [__stemmer.stem(t) for t in __tkr.tokenize(text)
                    if not t.startswith('@')]

def get_tokenized_corpus(corpus:list):
    dhash = hash_md5(list(corpus))
    dfile = model_tokenized_corpus+"-"+dhash+".npy"
    if os.path.isfile(dfile):
        print("[CORPUS] loading from file (dhash={})".format(dhash))
        return np.load(dfile)
    print("[CORPUS] generating (dhash={})...".format(dhash))
    tokenized_corpus = []
    for i, line in enumerate(corpus):
        tokens = __nltk_tokens(line)
        tokenized_corpus.append(tokens)
    np.save(dfile, tokenized_corpus)
    return tokenized_corpus

def str2vec(vec:list, text:str, max_length:int=20, vector_size:int=512):
    tokens = __nltk_tokens(text)
    X_1_input = np.zeros((1, max_length, vector_size), dtype=K.floatx())
    for t, token in enumerate(tokens):
        if t >= max_length:  break
        if token not in vec: continue
        # for debugging input (neural network)
        # print("token => {}".format(token))
        X_1_input[0, t, :] = vec[token]
    return X_1_input

import tensorflow as tf

def f1_score(y_true, y_pred):
    y_pred = K.round(y_pred)
    tp = K.sum(K.cast(y_true*y_pred, 'float'), axis=0)
    # tn = K.sum(K.cast((1-y_true)*(1-y_pred), 'float'), axis=0)
    fp = K.sum(K.cast((1-y_true)*y_pred, 'float'), axis=0)
    fn = K.sum(K.cast(y_true*(1-y_pred), 'float'), axis=0)

    p = tp / (tp + fp + K.epsilon())
    r = tp / (tp + fn + K.epsilon())

    f1 = 2*p*r / (p+r+K.epsilon())
    f1 = tf.where(tf.is_nan(f1), tf.zeros_like(f1), f1)
    return K.mean(f1)

Sequential    = tf.keras.models.Sequential
Dense         = tf.keras.layers.Dense
Dropout       = tf.keras.layers.Dropout
Flatten       = tf.keras.layers.Flatten
Conv1D        = tf.keras.layers.Conv1D
Adam          = tf.keras.optimizers.Adam

model_deep_personality = 'deep_person/model/deep_personality'

def DeepPersonality(max_length:int=20, vector_size:int=512):
    model = Sequential()

    model.add(Conv1D(32, kernel_size=3, activation='elu', padding='same',
        input_shape=(max_length, vector_size)))
    model.add(Conv1D(32, kernel_size=3, activation='elu', padding='same'))
    model.add(Conv1D(32, kernel_size=3, activation='elu', padding='same'))
    model.add(Conv1D(32, kernel_size=3, activation='elu', padding='same'))
    model.add(Dropout(0.25))

    model.add(Conv1D(32, kernel_size=2, activation='elu', padding='same'))
    model.add(Conv1D(32, kernel_size=2, activation='elu', padding='same'))
    model.add(Conv1D(32, kernel_size=2, activation='elu', padding='same'))
    model.add(Conv1D(32, kernel_size=2, activation='elu', padding='same'))
    model.add(Dropout(0.25))

    model.add(Flatten())

    model.add(Dense(256, activation='tanh'))
    model.add(Dense(256, activation='tanh'))
    model.add(Dropout(0.5))

    model.add(Dense(2, activation='softmax'))

    optimizer = Adam(lr=0.0001, decay=1e-6)

    model.compile(loss='hinge',
                  optimizer=optimizer,
                  metrics=[f1_score])

    # loss='categorical_crossentropy'
    # metrics=[f1_score, 'accuracy', tf.keras.metrics.mae]

    return model
