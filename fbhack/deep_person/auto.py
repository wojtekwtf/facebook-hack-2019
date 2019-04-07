import numpy as np
import pandas as pd

df1 = pd.read_pickle("deep_person/model/parsed_auto_dataset.bin")

import math
import numpy as np
#import matplotlib.pyplot as plt

def sigmoid(x):
    return 1 / (1 + math.exp(-x))

def simulate(val:float, prob:float, alpha:float, beta:float):
    X, Y = [], []
    for t in np.arange(2019, 2030, 1/4):
        X.append(t)
        r0_1 = np.random.uniform(prob/2-beta/1.5, alpha*prob)
        yprob = r0_1*(np.arctanh(min(0.99, prob+0.5)))
        zprob = np.sign(r0_1)*(abs(yprob))/10
        print(r0_1, zprob)
        bias = zprob*val   # new born?
        val = val - bias + val*0.0020 #+ val*r0_1
        #print("val={} prob={} bias={}".format(val, yprob, bias))
        Y.append(val)
        if val < 5: break
    return X, Y

def analyze_by_name(name:str):
    print("==> NAME", name)
    rows = df1.loc[df1['Occupation'].str.contains(name)]

    E1 = rows["Employment"].mean(axis=0)
    E2 = rows["Experienced Wage"].mean(axis=0)
    prob = rows["Probability"].mean(axis=0)

    print(E1, E2, prob)
    print(np.arctanh(prob))

    X, Y = simulate(E1, prob, alpha=0.95, beta=0.15)
    #plt.plot(X, Y)
    #plt.xlabel('Year')
    #plt.ylabel('Employment')
    #plt.show()

    """
    X, Y = simulate(E2, prob, alpha=0.93, beta=0.15)
    plt.plot(X, Y)
    plt.xlabel('Year')
    plt.ylabel('Experienced Wage')
    plt.show()
    """

    X, Y = simulate(E1, prob, alpha=0.95, beta=0.15)
    return Y[0] > Y[-1] - Y[0]*0.01

is_dying = analyze_by_name

analyze_by_name("Software Developers") # False
print(is_dying("Telemarketer"))        # True
#analyze_by_name("Telemarketer")