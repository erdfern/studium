import numpy as np

# a)
# samples = np.load("backup_data_2a.npy")
# print(data)
# print(data.mean())

rng = np.random.default_rng(101)

mean = np.array([0.0, 0.0])
cov = np.array([[1.0, 0.0], [0.0, 10.0]])
# cov = np.cov()

samples = rng.multivariate_normal(mean, cov, 2000, check_valid="raise")

# print(samples)
# print(data == samples)
# print(samples.T)


# b)
def get_rotation_matrix(theta):
    c = np.cos(theta)
    s = np.sin(theta)
    return np.array([[c, -s], [s, c]])


theta = np.radians(40)
r_matrix = get_rotation_matrix(theta)
# data_rotated = data @ r_matrix

r_matrix = get_rotation_matrix(theta)
samples_rotated = samples @ r_matrix
# samples_rotated = np.load("backup_data_2b.npy")

# c)
import matplotlib.pyplot as plt
import matplotlib.ticker as ticker

fig, axes = plt.subplots(1, 2, figsize=(12, 8))

# Plot our data
axes[0].scatter(samples[:, 0], samples[:, 1], s=8, color="navy")
axes[0].scatter(
    samples_rotated[:, 0], samples_rotated[:, 1], s=8, color="darkorange"
)
# Insert a marker for mean
mean_axs = axes[0].scatter(0, 0, marker="x", s=150, color="black", label="Mean")

# Disable top and right plot borders
axes[0].spines["top"].set_visible(False)
axes[0].spines["right"].set_visible(False)

# Axis labels
axes[0].set_xlabel("x")
axes[0].set_ylabel("y")

# Ticks in steps of {+-}5
axes[0].xaxis.set_ticks([tick for tick in axes[0].get_xticks() if tick % 5 == 0 and tick != 0])
axes[0].yaxis.set_ticks([tick for tick in axes[0].get_yticks() if tick % 5 == 0 and tick != 0])
# axes[0].yaxis.set_ticks(np.arange(start, end, 5))

# Show tick values as integers to discard any decimal places
axes[0].yaxis.set_major_formatter(ticker.FormatStrFormatter('%d'))

# Titles
axes[0].set_title("a)", fontsize=16, loc="left")
axes[0].set_title("Original and rotated point cloud")

# Set legend
axes[0].legend(loc="upper left", frameon=False)

axes[1].spines["top"].set_visible(False)
axes[1].spines["right"].set_visible(False)
orig_data = axes[1].hist(
    samples[:, 0],
    bins=111,
    # color="navy",
    fc=(1, 0.5, 0, 0.5),
    zorder=1,
    label="Original data",
)
rot_data = axes[1].hist(
    samples_rotated[:, 0],
    bins=111,
    # color="darkorange",
    fc=(0.118, 0.25, 0.35, 0.5),
    zorder=0,
    label="Rotated data",
)
axes[1].set_ylabel("Count")
axes[1].set_xlabel("x")

axes[1].yaxis.set_major_formatter(ticker.FormatStrFormatter('%d'))

axes[1].xaxis.set_ticks([tick for tick in axes[1].get_xticks() if tick % 5 == 0])
axes[1].yaxis.set_ticks([tick for tick in axes[1].get_yticks() if tick % 5 == 0])

axes[1].set_title("b)", fontsize=16, loc="left")
axes[1].set_title("Histogram of the x dimension")

axes[1].legend(loc="center left", frameon=False)

# plt.tight_layout()
# plt.show()
plt.savefig("icry.jpg")
