from scipy.stats import shapiro, levene, mannwhitneyu
import matplotlib.pyplot as plt

group1 = [
    6.2,
    7.1,
    1.5,
    2.3,
    2,
    1.5,
    6.1,
    2.4,
    2.3,
    12.4,
    1.8,
    5.3,
    3.1,
    9.4,
    2.3,
    4.1,
]
group2 = [
    2.3,
    2.1,
    1.4,
    2.0,
    8.7,
    2.2,
    3.1,
    4.2,
    3.6,
    2.5,
    3.1,
    6.2,
    12.1,
    3.9,
    2.2,
    1.2,
    3.4,
]


# 3.2.1): Hypotheses and Group Independence

# H0 (Null Hypothesis): The mean time to solve homework is the same for both groups.
# H1 (Alternative Hypothesis): The mean time to solve homework is different for the two groups.

# The groups are independent (unpaired) because there is no inherent pairing or matching between the individuals in group1 and group2.

# 3.2.a)
alpha = 0.05

_, p_value_group1 = shapiro(group1)
_, p_value_group2 = shapiro(group2)

print(f"Shapiro-Wilk Test (Group 1): p-value = {p_value_group1:.4f}")
print(f"Shapiro-Wilk Test (Group 2): p-value = {p_value_group2:.4f}")

if p_value_group1 > alpha and p_value_group2 > alpha:
    print("We cannot reject the null hypothesis of normality for both groups.")
else:
    print("At least one of the groups does not follow a normal distribution.")


# 3.2.b) Homogeneity
_, p_value_levene = levene(group1, group2)

print(f"Levene's Test: p-value = {p_value_levene:.4f}")

if p_value_levene > alpha:
    print("We cannot reject the null hypothesis of equal variances.")
else:
    print("The groups have significantly different variances.")

# 3.3)
_, p_value_mannwhitneyu = mannwhitneyu(group1, group2)
print(f"\nMann-Whitney U Test: p-value = {p_value_mannwhitneyu:.4f}")

if p_value_mannwhitneyu > alpha:
    print(
        "Fail to reject the null hypothesis. There is no significant difference in the median time to complete homework between the two groups."
    )
else:
    print(
        "Reject the null hypothesis. There is a significant difference in the median time to complete homework between the two groups."
    )

# Box plots for each group
plt.figure(figsize=(10, 6))
plt.boxplot([group1, group2], labels=["Group 1", "Group 2"])
plt.title("Box Plot Comparison of Homework Completion Times")
plt.ylabel("Time")
plt.show()
