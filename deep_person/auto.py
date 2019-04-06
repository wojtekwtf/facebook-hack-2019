import pandas as pd

COLUMNS_1 = """
Alabama,Alaska,Arizona,Arkansas,California,Colorado,Connecticut,
Delaware,District of Columbia,Florida,Georgia,Hawaii,Idaho,Illinois,Indiana,Iowa,
Kansas,Kentucky,Louisiana,Maine,Maryland,Massachusetts,Michigan,Minnesota,
Mississippi,Missouri,Montana,Nebraska,Nevada,New Hampshire,New Jersey,New Mexico,
New York,North Carolina,North Dakota,Ohio,Oklahoma,Oregon,Pennsylvania,
Rhode Island,South Carolina,South Dakota,Tennessee,Texas,Utah,Vermont,
Virginia,Washington,West Virginia,Wisconsin,Wyoming""".replace("\n", "").split(",")

print(COLUMNS_1)

COLUMNS_2 = """
Area Type,Area,Area Name,Mean Wage,Median Wage,Entry Wage""".replace("\n",
        "").split(",")

print(COLUMNS_2)

def soc_column(row: object):
    return row['SOC'].strip()[0:6]

def e1_column(row: object):
    return df2.loc[df2['SOC'] == row['SOC']]["Employment"].mean(axis=0)

def e2_column(row: object):
    return df2.loc[df2['SOC'] == row['SOC']]["Experienced Wage"].mean(axis=0)

df1 = pd.read_csv("data/raw_state_automation_data.csv",
        sep=",", encoding='cp1252')
df1 = df1.drop(COLUMNS_1, 1)
df1['SOC'] = df1.apply(soc_column, axis=1)
print(df1.head())

df2 = pd.read_csv("data/occupational-employment-statistics.csv",
        sep=",", encoding='cp1252')
df2 = df2.rename(columns={'Standard Occupational Code': 'SOC'})
df2 = df2.drop(COLUMNS_2, 1)
df2['SOC'] = df2.apply(soc_column, axis=1)
df2 = df2[df2["SOC"] != "00-000"]
print(df2.head())

df1['Employment'] = df1.apply(e1_column, axis=1)
df1['Experienced Wage'] = df1.apply(e2_column, axis=1)
print(df1.head())

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
