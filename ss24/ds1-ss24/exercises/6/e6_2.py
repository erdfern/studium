import numpy as np
import matplotlib.pyplot as plt
from scipy.stats import norm, bootstrap

# Parameters for the Gaussian distribution
mean = 10
std_dev = 3

# Sample sizes
sample_sizes = [100, 1000, 10000]

# Generate samples
samples_100 = norm.rvs(loc=mean, scale=std_dev, size=100)
samples_1000 = norm.rvs(loc=mean, scale=std_dev, size=1000)
samples_10000 = norm.rvs(loc=mean, scale=std_dev, size=10000)

# Plot histograms
fig, axs = plt.subplots(3, 1, figsize=(10, 15))

# Plot PDF for the distribution
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

# 2.3) load sample.npy
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

# 2.4) null hypothesis is that mean is equal to 5. Alternative hypothesis is that it's not. Reject H0? Use bootstrapping.
