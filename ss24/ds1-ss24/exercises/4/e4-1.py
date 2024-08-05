import pandas as pd

# df = pd.read_csv("tips.csv")
df = pd.read_csv(
    "https://raw.githubusercontent.com/mwaskom/seaborn-data/master/tips.csv"
)
print(df.shape)

print(df.columns)

# Check if each dtype is numeric
data_types = df.dtypes
count_numeric = 0
# TODO use a list comprehension instead
for col, dtype in data_types.items():
    is_numeric = pd.api.types.is_numeric_dtype(dtype)
    if is_numeric:
        count_numeric += 1
    print(f"{col} is numeric: {is_numeric}")

print(
    f"Numeric columns: {count_numeric}, other: {len(data_types) - count_numeric}"
)

# Calculate the average bill for table
mean_bill = df["total_bill"].mean(numeric_only=True)
print(mean_bill)

import seaborn as sns

sns.set_theme()  # make it pretty

sns.scatterplot(data=df, x="total_bill", y="tip", hue="tip")

# Calculate mean tip by sex
mean_tip_by_sex = df.groupby("sex")["tip"].mean()
mean_tip_male = mean_tip_by_sex["Male"]
mean_tip_female = mean_tip_by_sex["Female"]
print(f"Mean tip by sex:\nFemale: {mean_tip_female}\nMale: {mean_tip_male}")
