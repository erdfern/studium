import numpy as np
import matplotlib.pyplot as plt
from utils import color1, color2


# src: https://stackoverflow.com/a/26757297
def cartesian_to_polar(x, y):
    r = np.sqrt(x**2 + y**2)
    theta = np.arctan2(y, x)
    return r, theta


def transform_and_plot_polar(samples, labels, color1, color2):
    # Transform to polar coordinates
    r, theta = cartesian_to_polar(samples[:, 0], samples[:, 1])

    # Separate data points based on labels
    r_0 = r[labels == 0]
    theta_0 = theta[labels == 0]
    r_1 = r[labels == 1]
    theta_1 = theta[labels == 1]

    # Create polar plot
    _, ax = plt.subplots(figsize=(10, 10), subplot_kw=dict(projection="polar"))

    ax.scatter(theta_0, r_0, c=color1, label="Label 0")
    ax.scatter(theta_1, r_1, c=color2, label="Label 1")

    ax.set_title("Polar Plot of Samples by Label")
    ax.legend()

    plt.show()


samples = np.load("ex2_samples.npy")
labels = np.load("ex2_labels.npy")


transform_and_plot_polar(samples, labels, color1, color2)
