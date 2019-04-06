"""
Session:
$ python3 train.py cEXT,cNEU,cAGR,cCON,cOPN

Debug:
$ tensorboard --logdir logs/
             vs.
$ python3 /Users/maciejczyzewski/.pyenv/versions/3.7.2/lib/python3.7/site-packages/tensorboard/main.py --logdir logs/
"""

import session

from glob import glob
import sys, multiprocessing

import tensorflow as tf
EarlyStopping = tf.keras.callbacks.EarlyStopping

from model import DeepPersonality
from model import model_deep_personality
from data  import get_training_data, dataset_mypersonality

TRAITS = sys.argv[1].split(",")
print("[\033[92m{}\033[0m]".format(TRAITS))

nb_epochs = 100; batch_size = 32

model = DeepPersonality()
dataset = dataset_mypersonality()

def get_model_name(trait:str):
    return model_deep_personality+"_"+trait

tbCallBack = tf.keras.callbacks.TensorBoard(log_dir='logs/', histogram_freq=0, write_graph=True, write_images=True)

while True:
    for trait in TRAITS:
        print("[\033[92m{}\033[0m]".format(trait))
        X_train, Y_train, X_test, Y_test = get_training_data(dataset, trait)

        if glob(get_model_name(trait)+"*") != []:
            print("[DEEP_PERSONALITY] loading weights")
            model.load_weights(get_model_name(trait))

        model.fit(X_train, Y_train,
                  batch_size=batch_size,
                  shuffle=True,
                  epochs=nb_epochs,
                  validation_data=(X_test, Y_test),
                  callbacks=[#tbCallBack,
                      EarlyStopping(min_delta=0.00025, patience=2)])

        model.save_weights(get_model_name(trait))
