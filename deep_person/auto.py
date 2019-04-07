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

df1.to_pickle("model/parsed_auto_dataset.bin")
