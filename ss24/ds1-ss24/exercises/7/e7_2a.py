import numpy as np
import matplotlib.pyplot as plt
from utils import color1, color2
from lib import cartesian_to_polar


def plot_samples(samples, labels, color1, color2, projection=None):
    r, theta = cartesian_to_polar(samples[:, 0], samples[:, 1])

    r_0 = r[labels == 0]
    theta_0 = theta[labels == 0]
    r_1 = r[labels == 1]
    theta_1 = theta[labels == 1]

    _, ax = plt.subplots(
        figsize=(10, 10), subplot_kw=dict(projection=projection)
    )

    ax.scatter(theta_0, r_0, c=color1, label="Label 0")
    ax.scatter(theta_1, r_1, c=color2, label="Label 1")

    ax.set_title("Polar Plot of Samples by Label")
    ax.legend()

    plt.show()


samples = np.load("ex2_samples.npy")
labels = np.load("ex2_labels.npy")

# projection : {None, 'aitoff', 'hammer', 'lambert', 'mollweide', 'polar', 'rectilinear', str}
plot_samples(samples, labels, color1, color2, "polar")
plot_samples(samples, labels, color1, color2)
