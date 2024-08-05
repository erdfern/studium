# a) (5%) Load the “samples.npy” and “labels.npy”. Visualize the samples in a scatterplot with the imported colors "color1" and "color2" for the different labels.
import numpy as np
import matplotlib.pyplot as plt

from utils import color1, color2, custom_cmap

samples = np.load("samples.npy")

labels = np.load("labels.npy")

# Separate data points based on labels
samples_0 = samples[labels == 0]
samples_1 = samples[labels == 1]

plt.figure(figsize=(8, 6))

plt.scatter(samples_0[:, 0], samples_0[:, 1], c=color1, label="Label 0")

plt.scatter(samples_1[:, 0], samples_1[:, 1], c=color2, label="Label 1")

plt.xlabel("X")
plt.ylabel("Y")
plt.title("Scatter Plot of Samples by Label")
plt.legend()

plt.grid(True)
plt.show()


# a) (5%) Load the “samples.npy” and “labels.npy”. Visualize the samples in a scatterplot with the imported colors "color1" and "color2" for the different labels.
from sklearn.neighbors import KNeighborsClassifier
from sklearn.model_selection import train_test_split
from sklearn.metrics import accuracy_score

x_train, x_test, y_train, y_test = train_test_split(
    samples, labels, test_size=0.2, random_state=42
)

knn = KNeighborsClassifier(n_neighbors=2)  # k=2
knn.fit(x_train, y_train)

y_pred = knn.predict(x_test)

accuracy = accuracy_score(y_test, y_pred)
print(f"Accuracy of KNN (k=2): {accuracy:.2f}")

# c) (15%) Plot the fitted classification limits from b) into your figure from a).
# *Hint: Create a grid using `np.meshgrid`, then let your fitted KNeighborsClassifier classify each point. Plot the result using plt.imshow. You can use the imported “custom_cmap” as cmap.*

def plot_classification(samples, split_samples, classifier):
    h = 0.02  # Step size in the mesh
    x_min, x_max = samples[:, 0].min() - 1, samples[:, 0].max() + 1
    y_min, y_max = samples[:, 1].min() - 1, samples[:, 1].max() + 1
    xx, yy = np.meshgrid(
        np.arange(x_min, x_max, h), np.arange(y_min, y_max, h)
    )

    # precidt labels for the meshgrid
    Z = classifier.predict(np.c_[xx.ravel(), yy.ravel()])
    Z = Z.reshape(xx.shape)

    # plot the decisiwillon classification limits
    plt.figure(figsize=(8, 6))
    plt.contourf(xx, yy, Z, cmap="inferno", alpha=0.8)

    # plot the original scatter plot
    plt.scatter(
        split_samples[0][:, 0],
        split_samples[0][:, 1],
        c=color1,
        label="Label 0",
    )
    plt.scatter(
        split_samples[1][:, 0],
        split_samples[1][:, 1],
        c=color2,
        label="Label 1",
    )

    plt.xlabel("X")
    plt.ylabel("Y")
    plt.title(
        "Scatter Plot of Samples by Label with KNN Decision Boundary (k=2)"
    )
    plt.legend()
    plt.grid(True)
    plt.show()


plot_classification(samples, (samples_0, samples_1), knn)


# d) (5%) You will notice small islands in the classification boundaries. What is the smallest value of k at which the islands disappear? For which value of k is the accuracy best?
# TODO

# e) (5%) Load the test data “samples_test.npy” and “labels_test.npy” and calculate the accuracy for these too. What do you notice?

samples_test = np.load("samples_test.npy")
labels_test = np.load("labels_test.npy")

# 20/80 split again
x_train_2, x_test_2, y_train_2, y_test_2 = train_test_split(
    samples_test, labels_test, test_size=0.2, random_state=42
)

knn = KNeighborsClassifier(n_neighbors=2)  # k=2
knn.fit(x_train_2, y_train_2)

y_pred_2 = knn.predict(x_test_2)

accuracy = accuracy_score(y_test_2, y_pred_2)
print(f"Accuracy of KNN (k=2): {accuracy:.2f}")


# f) (10%) Fit the data with a LogisticRegression from sklearn and create a plot like in c), one with the continuous classification "limits" and one with hard limits (threshold at 0.5). Compare the training and test accuracies. How are the results different from those of your KNeighborsClassifier?
from sklearn.linear_model import LogisticRegression
import numpy as np
import matplotlib.pyplot as plt
from sklearn.metrics import accuracy_score

# Fit LogisticRegression
logit = LogisticRegression(random_state=42)
logit.fit(x_train, y_train)


# Function to plot decision boundaries
def plot_decision_boundary(classifier, X, y, is_probability=False):
    h = 0.02
    x_min, x_max = X[:, 0].min() - 1, X[:, 0].max() + 1
    y_min, y_max = X[:, 1].min() - 1, X[:, 1].max() + 1
    xx, yy = np.meshgrid(
        np.arange(x_min, x_max, h), np.arange(y_min, y_max, h)
    )

    if is_probability:
        Z = classifier.predict_proba(np.c_[xx.ravel(), yy.ravel()])[:, 1]
    else:
        Z = classifier.predict(np.c_[xx.ravel(), yy.ravel()])
    Z = Z.reshape(xx.shape)

    plt.figure(figsize=(10, 8))
    if is_probability:
        plt.contourf(xx, yy, Z, cmap=custom_cmap, alpha=0.8)
    else:
        plt.contourf(
            xx, yy, Z, cmap=custom_cmap, alpha=0.8, levels=[0, 0.5, 1]
        )

    plt.scatter(X[y == 0][:, 0], X[y == 0][:, 1], c=color1, label="Label 0")
    plt.scatter(X[y == 1][:, 0], X[y == 1][:, 1], c=color2, label="Label 1")

    plt.xlabel("X")
    plt.ylabel("Y")
    plt.title(
        "Logistic Regression Decision Boundary"
        + (" (Probability)" if is_probability else "")
    )
    plt.legend()
    plt.show()


# Plot continuous classification limits
plot_decision_boundary(logit, samples, labels, is_probability=True)

# Plot hard classification limits
plot_decision_boundary(logit, samples, labels, is_probability=False)

# same for KNN
# TODO decide which plot function to use for KNN.
# plot_decision_boundary(knn, samples, labels, is_probability=False)

# Calculate accuracies
y_train_pred = logit.predict(x_train)
y_test_pred = logit.predict(x_test)

train_accuracy = accuracy_score(y_train, y_train_pred)
test_accuracy = accuracy_score(y_test, y_test_pred)

print(f"Logistic Regression - Training Accuracy: {train_accuracy:.4f}")
print(f"Logistic Regression - Test Accuracy: {test_accuracy:.4f}")

# Compare with KNeighborsClassifier
knn = KNeighborsClassifier(n_neighbors=2)
knn.fit(x_train, y_train)

knn_train_pred = knn.predict(x_train)
knn_test_pred = knn.predict(x_test)

knn_train_accuracy = accuracy_score(y_train, knn_train_pred)
knn_test_accuracy = accuracy_score(y_test, knn_test_pred)

print(f"KNeighborsClassifier - Training Accuracy: {knn_train_accuracy:.4f}")
print(f"KNeighborsClassifier - Test Accuracy: {knn_test_accuracy:.4f}")
