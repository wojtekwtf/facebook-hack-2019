import numpy as np
import tensorflow as tf
import tensorflow.keras.backend as K

import multiprocessing

use_gpu = True

config = tf.ConfigProto(
    intra_op_parallelism_threads=multiprocessing.cpu_count(),
    inter_op_parallelism_threads=multiprocessing.cpu_count(),
    allow_soft_placement=True,
    device_count = {'CPU' : 3,
                    'GPU' : 1 if use_gpu else 0})

session = tf.Session(config=config)
K.set_session(session)

np.random.seed(1002)
