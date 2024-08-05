import numpy as np
import matplotlib.pyplot as plt
from sklearn.neighbors import KNeighborsClassifier
from utils import color1, color2


def cartesian_to_polar(x, y):
    r = np.sqrt(x**2 + y**2)
    theta = np.arctan2(y, x)
    return np.column_stack((r, theta))


def calculate_accuracy(true_labels, predicted_labels):
    correct_predictions = np.sum(true_labels == predicted_labels)
    total_predictions = len(true_labels)
    return correct_predictions / total_predictions


ex2_samples_train = np.load("ex2_samples.npy")
ex2_labels_train = np.load("ex2_labels.npy")
ex2_samples_test = np.load("ex2_samples_test.npy")
ex2_labels_test = np.load("ex2_labels_test.npy")

samples_train_polar = cartesian_to_polar(
    ex2_samples_train[:, 0], ex2_samples_train[:, 1]
)
samples_test_polar = cartesian_to_polar(ex2_samples_test[:, 0], ex2_samples_test[:, 1])

k_values = range(1, 21)  # Testing k from 1 to 20

train_accuracy = []
test_accuracy = []

for k in k_values:
    knn = KNeighborsClassifier(n_neighbors=k)
    knn.fit(samples_train_polar, ex2_labels_train)

    train_pred = knn.predict(samples_train_polar)
    train_acc = calculate_accuracy(ex2_labels_train, train_pred)
    train_accuracy.append(train_acc)

    test_pred = knn.predict(samples_test_polar)
    test_acc = calculate_accuracy(ex2_labels_test, test_pred)
    test_accuracy.append(test_acc)

plt.figure(figsize=(10, 6))
plt.plot(k_values, train_accuracy, label="Training Accuracy", marker="o", color=color1)
plt.plot(k_values, test_accuracy, label="Test Accuracy", marker="s", color=color2)
plt.xlabel("k (Number of Neighbors)")
plt.ylabel("Accuracy")
plt.title("k vs Accuracy for KNN Classifier")
plt.legend()
plt.grid(True)
plt.show()

best_k = k_values[np.argmax(test_accuracy)]
print(f"The best k value based on test accuracy is: {best_k}")
