import numpy as np
import matplotlib.pyplot as plt
from scipy.stats import norm, bootstrap

# 2.1) Defining the gaussian distribution

# Parameters for the Gaussian distribution
mean = 10
std_dev = 3

sample_sizes = [100, 1000, 10000]

samples_100 = norm.rvs(loc=mean, scale=std_dev, size=100)
samples_1000 = norm.rvs(loc=mean, scale=std_dev, size=1000)
samples_10000 = norm.rvs(loc=mean, scale=std_dev, size=10000)

fig, axs = plt.subplots(3, 1, figsize=(10, 15))

x = np.linspace(mean - 4 * std_dev, mean + 4 * std_dev, 1000)
pdf = norm.pdf(x, loc=mean, scale=std_dev)

# Histogram for 100 samples
axs[0].hist(
    samples_100,
    bins=30,
    density=True,
    alpha=0.6,
    color="b",
    label="Histogram (n=100)",
)
axs[0].plot(x, pdf, "r-", lw=2, label="PDF")
axs[0].set_title("Sampling Distribution with n=100")
axs[0].set_xlabel("Value")
axs[0].set_ylabel("Frequency")
axs[0].legend()

# Histogram for 1000 samples
axs[1].hist(
    samples_1000,
    bins=30,
    density=True,
    alpha=0.6,
    color="g",
    label="Histogram (n=1000)",
)
axs[1].plot(x, pdf, "r-", lw=2, label="PDF")
axs[1].set_title("Sampling Distribution with n=1000")
axs[1].set_xlabel("Value")
axs[1].set_ylabel("Frequency")
axs[1].legend()

# Histogram for 10000 samples
axs[2].hist(
    samples_10000,
    bins=30,
    density=True,
    alpha=0.6,
    color="m",
    label="Histogram (n=10000)",
)
axs[2].plot(x, pdf, "r-", lw=2, label="PDF")
axs[2].set_title("Sampling Distribution with n=10000")
axs[2].set_xlabel("Value")
axs[2].set_ylabel("Frequency")
axs[2].legend()

plt.tight_layout()
plt.show()

# 2.2) Difference between the standard derivation of the sampling distribution and the standard derivation of the underlying gaussian distribution.


# The standard deviation of the underlying Gaussian distribution ($\sigma$) represents the spread of the individual data points around the mean of the population. In this case, it is given as 3.

# The standard deviation of the sampling distribution measures the variability of the sample means around the true population mean. This is given by:
# $\text{Standard Error} = \frac{\sigma}{\sqrt{n}}$

# This formula shows that the standard error decreases as the sample size $n$ increases. Essentially, with larger sample sizes, the sample means are expected to be closer to the population mean, reducing the variability of the sample means.

# ### Empirical Results:

# In the histograms:

# 1. **Small Sample Size (n = 100):**
#    - The histogram is broader and less smooth, reflecting greater variability in the sample means. more precise estimates of the population mean.

#    - The broader shape indicates a higher standard error, meaning the sample means are more spread out around the true mean.

# 2. **Medium Sample Size (n = 1000):**
#    - The histogram is narrower and smoother compared to $n = 100$.
#    - This shows a reduced standard error, indicating that the sample means are less spread out and more tightly clustered around the true mean.

# 3. **Large Sample Size (n = 10000):**
#    - The histogram is the narrowest and smoothest of all three.
#    - This reflects the smallest standard error, meaning the sample means are very close to the true mean and show minimal spread.

# ### Visual Representation:

# - **Broader Histograms (Small $n$)**: Larger variability in sample means, higher standard error.
# - **Narrower Histograms (Large $n$)**: Smaller variability in sample means, lower standard error.

# As the sample size increases, the histograms become more concentrated around the mean (10), and their shape increasingly resembles the PDF of the Gaussian distribution, illustrating the reduced variability in the sample means.

# 2.3) Load sample.npy
sample = np.load("sample.npy")
empirical_mean = sample.mean()
sample = (sample,)
print(sample)

# calculate 95% bootstrapped confidence interval for mean
bootstrap_ci = bootstrap(
    sample, np.mean, confidence_level=0.95, random_state=1, method="percentile"
)

print(f"95% confidence interval for mean: {bootstrap_ci.confidence_interval}")
print(f"Empirical mean: {empirical_mean}")

# 2.4)
null_hypothesis_mean = 5
shifted_sample = sample[0] - null_hypothesis_mean  # Shift the data to center it around 0

# Perform bootstrapping
bootstrap_results = bootstrap(
    (shifted_sample,),
    np.mean,
    confidence_level=0.95,  # 95% confidence for a two-tailed test
    n_resamples=10000,       # Generate 10000 bootstrap samples
    random_state=1,
    method="percentile",
)

# We get the critical values (2.5% and 97.5% percentiles)
lower_critical_value = bootstrap_results.confidence_interval[0]
upper_critical_value = bootstrap_results.confidence_interval[1]

# Test statistic: Absolute difference between empirical mean and null hypothesis mean
observed_test_statistic = abs(empirical_mean - null_hypothesis_mean)

# Decision
if observed_test_statistic > upper_critical_value or observed_test_statistic < lower_critical_value:
    print("Reject the null hypothesis (H0).")
else:
    print("Fail to reject the null hypothesis (H0).")
