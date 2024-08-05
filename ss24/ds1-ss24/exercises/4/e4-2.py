import pandas as pd
import numpy as np

# b)
df = pd.read_csv("cleaned_titanic.csv", sep=";")

# df.info()

# c)
print(df.Sex.unique())

# d)
# Further cleaning
# valid_sex_entries = ["male", 'female', "mal", "femal", "mle"]
valid_sex_entries = ["male", "female"]
# Convert all entries to lowercase for comparison
df.Sex = df.Sex.astype(str).str.lower()

# Replace invalid entries with NaN
df.loc[~df.Sex.isin(valid_sex_entries), "Sex"] = np.nan

# Fill NaN values with ''
# df["Sex"] = df["Sex"].fillna('')

df.Sex = df.Sex.replace({"male": "m", "female": "f"})

# e)
df.Name = df.Name.str.replace(r';(.*?)\.', ';', regex=True)

# print(df)

# Example
# exdf = pd.read_csv("https://raw.githubusercontent.com/mwaskom/seaborn-data/master/titanic.csv")

# df.info()
# exdf.info()
