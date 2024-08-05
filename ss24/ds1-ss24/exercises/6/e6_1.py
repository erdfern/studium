import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt

titanic_df = pd.read_csv("titanic.csv")

# Calculate the average fare per class
average_fare_per_class = titanic_df.groupby('pclass')['fare'].mean().reset_index()

# Create a barplot
plt.figure(figsize=(10, 6))
barplot = sns.barplot(data=average_fare_per_class, x='pclass', y='fare', hue='pclass', palette='viridis')

# Annotate the barplot with the average fare values
for index, row in average_fare_per_class.iterrows():
    barplot.text(row['pclass']-1, row['fare'], round(row['fare'], 2), color='black', ha="center")

plt.title('Average Ticket Price per Class')
plt.xlabel('Class')
plt.ylabel('Average Fare')
plt.xticks([0, 1, 2], ['First', 'Second', 'Third'])
plt.show()

average_fare_per_class.info()

import numpy as np

median_fare_per_class = titanic_df.groupby('pclass')['fare'].median().reset_index()

# Create a barplot for median fares using np.median as the estimator
plt.figure(figsize=(10, 6))
barplot_median = sns.barplot(data=titanic_df, x='pclass', y='fare', estimator=np.median, hue='pclass', palette='viridis')

# Annotate the barplot with the median fare values
for index, row in median_fare_per_class.iterrows():
    barplot_median.text(row['pclass']-1, row['fare'], round(row['fare'], 2), color='black', ha="center")

plt.title('Median Ticket Price per Class')
plt.xlabel('Class')
plt.ylabel('Median Fare')
plt.xticks([0, 1, 2], ['First', 'Second', 'Third'])
plt.show()

median_fare_per_class
