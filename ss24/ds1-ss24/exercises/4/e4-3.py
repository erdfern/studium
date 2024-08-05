import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt

# Load the dataset
df = pd.read_csv(
    "https://raw.githubusercontent.com/mwaskom/seaborn-data/master/titanic.csv"
)

# 2 a)
# Some statistical measures
# Describing central tendency
age_mean = df["age"].mean()
age_median = df["age"].median()
# Describing dispersion
age_min = df["age"].min()
age_max = df["age"].max()
age_range = age_max - age_min
age_std_dev = df["age"].std()
# Describing shape
age_skew = df["age"].skew()

# Create a column indicating whether a passenger is below or above mean age
df["age_group"] = [
    "below_mean" if age < age_mean else "above_mean" for age in df["age"]
]

# Histogram with KDE
sns.displot(kind="hist", data=df, x="age", hue='age_group', kde=True, binwidth=1)
# Mark mean with a vertical line
plt.axvline(
    age_mean,
    color="red",
    linestyle="dashed",
    linewidth=1,
    label=f"Mean Age: {age_mean:.2f}",
)
plt.title("Age Distribution of Passengers")
plt.xlabel("Age")
plt.ylabel("Count")

# Create empty plot with blank marker containing the statistical measures to display in legend
plt.plot(
    [],
    [],
    " ",
    label=f"Median: {age_median:.2f}\nStd. Dev: {age_std_dev:.2f}\nRange: {age_range} ({age_min}...{age_max})\nSkewedness: {age_skew:.2f}",
)
plt.legend()

plt.show()

# b)
percent_below_mean = (df["age"] < age_mean).mean() * 100
percent_above_mean = (df["age"] >= age_mean).mean() * 100
labels = ["Below Mean", "Above Mean"]
sizes = [percent_below_mean, percent_above_mean]
colors = ["skyblue", "lightcoral"]

plt.pie(sizes, labels=labels, colors=colors, autopct="%1.1f%%", startangle=140)
plt.title("Proportion of Passengers Below vs. Above Mean Age")

plt.show()

# c)
df_agg = (
    df.groupby(["sex", "age_group"]).size().reset_index(name="count")
).pivot(index="sex", columns="age_group", values="count")

# Handle potential KeyError if a group is missing
df_agg = df_agg.fillna(0)  # Fill missing values with 0

total_passengers = df_agg.sum(axis=1)
df_agg_pct = df_agg.div(total_passengers, axis=0) * 100

ax = df_agg_pct.plot(kind="bar", stacked=True, color=["skyblue", "lightcoral"])
plt.title("Proportion of Passengers Below vs. Above Mean Age by Sex")
plt.ylabel("Percentage (%)")
plt.xlabel("Sex")

# Add percentage labels inside bars
for bar in ax.patches:
    width, height = bar.get_width(), bar.get_height()
    x, y = bar.get_xy()
    ax.text(
        x + width / 2,
        y + height / 2,
        f"{height:.1f}%",
        ha="center",
        va="center",
        color="black",
    )

plt.show()

# d)
survival_rate = df.groupby('sex')['survived'].mean() * 100

ax = survival_rate.plot(kind='bar', color=['skyblue', 'lightcoral'])
plt.title('Survival Rate by Gender')
plt.ylabel('Survival Rate (%)')
plt.xlabel('Gender')

# Add percentage labels on bars
for bar in ax.patches:
    height = bar.get_height()
    ax.text(
        bar.get_x() + bar.get_width() / 2,
        height,
        f'{height:.1f}%',
        ha='center',
        va='bottom',
        color='black'
    )

plt.show()

# e)
avg_fare_by_class = df.groupby('class')['fare'].mean()

print("Average Fare by Class:")
print(avg_fare_by_class)

sns.boxplot(x='class', y='fare', hue='class', data=df)
plt.title('Ticket Price Distribution by Class')
plt.xlabel('Class')
plt.ylabel('Fare')
plt.show()

# f)
survival_rate_by_class = df.groupby('class')['survived'].mean() * 100

print("Survival Rate by Class:")
print(survival_rate_by_class)

ax = survival_rate_by_class.plot(kind='bar', color=['skyblue', 'lightcoral', 'lightgreen'])
plt.title('Survival Rate by Class')
plt.ylabel('Survival Rate (%)')
plt.xlabel('Class')

for bar in ax.patches:
    height = bar.get_height()
    ax.text(
        bar.get_x() + bar.get_width() / 2,
        height,
        f'{height:.1f}%',
        ha='center',
        va='bottom',
        color='black'
    )

plt.show()
