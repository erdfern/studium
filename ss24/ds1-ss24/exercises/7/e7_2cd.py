import numpy as np
import matplotlib.pyplot as plt
from sklearn.neighbors import KNeighborsClassifier
from utils import color1, color2


def cartesian_to_polar(x, y):
    r = np.sqrt(x**2 + y**2)
    theta = np.arctan2(y, x)
    return np.column_stack((r, theta))


def calculate_accuracy(true_labels, predicted_labels):
    """
    Calculate the accuracy of predictions.

    Args:
    true_labels (array-like): The true labels
    predicted_labels (array-like): The predicted labels

    Returns:
    float: The accuracy as a value between 0 and 1
    """
    # NOTE could add checks that both arrays have same shape etc
    # get correct predictions via element-wise comparison of true labels with predictions
    correct_predictions = np.sum(true_labels == predicted_labels)
    total_predictions = len(true_labels)
    return correct_predictions / total_predictions


def generate_splits(n_samples, n_splits, random_state=None):
    """
    Generate indices for cross-validation splits.

    Args:
    n_samples (int): Total number of samples
    n_splits (int): Number of splits for cross-validation
    random_state (int): Controls the randomness of the splits

    Returns: List of tuples (train_indices, val_indices)
    """
    fold_size = n_samples // n_splits
    indices = np.arange(n_samples)

    if random_state is not None:
        np.random.seed(random_state)
        np.random.shuffle(indices)

    splits = []
    for i in range(n_splits):
        start = i * fold_size
        end = start + fold_size if i < n_splits - 1 else n_samples

        val_indices = indices[start:end]
        train_indices = np.concatenate([indices[:start], indices[end:]])

        splits.append((train_indices, val_indices))

    return splits


def custom_cross_val_score(X, y, clf, n_splits=5, random_state=None):
    """
    Perform cross-validation and return scores.

    Args:
    X (array-like): The input samples
    y (array-like): The target values
    clf: The classifier object
    n_splits (int): Number of splits for cross-validation
    random_state (int): Controls the randomness of each fold

    Returns: list of scores
    """
    splits = generate_splits(len(X), n_splits, random_state)
    scores = []

    for train_indices, val_indices in splits:
        X_train, X_val = X[train_indices], X[val_indices]
        y_train, y_val = y[train_indices], y[val_indices]

        clf.fit(X_train, y_train)
        y_pred = clf.predict(X_val)
        score = calculate_accuracy(y_val, y_pred)
        scores.append(score)

    return np.array(scores)


# Load and preprocess the data
samples_train = np.load("ex2_samples.npy")
labels_train = np.load("ex2_labels.npy")
samples_test = np.load("ex2_samples_test.npy")
labels_test = np.load("ex2_labels_test.npy")

samples_train_polar = cartesian_to_polar(
    samples_train[:, 0], samples_train[:, 1]
)
samples_test_polar = cartesian_to_polar(samples_test[:, 0], samples_test[:, 1])

# Define the range of k values to test
k_values = range(1, 21)  # Testing k from 1 to 20

# Perform cross-validation
n_splits = 5
cv_scores_mean = []
cv_scores_std = []

for k in k_values:
    knn = KNeighborsClassifier(n_neighbors=k)
    scores = custom_cross_val_score(
        samples_train_polar,
        labels_train,
        knn,
        n_splits=n_splits,
        random_state=42,
    )
    cv_scores_mean.append(scores.mean())
    cv_scores_std.append(scores.std())

# Find the best k value based on cross-validation
best_k_cv = k_values[np.argmax(cv_scores_mean)]
print(f"The best k value based on cross-validation is: {best_k_cv}")

# Train the final model with the best k from cross-validation
best_knn_cv = KNeighborsClassifier(n_neighbors=best_k_cv)
best_knn_cv.fit(samples_train_polar, labels_train)

# Evaluate on the test set
test_pred_cv = best_knn_cv.predict(samples_test_polar)
test_accuracy_cv = calculate_accuracy(labels_test, test_pred_cv)
print(
    f"Test accuracy with best k from cross-validation (k={best_k_cv}): {test_accuracy_cv:.4f}"
)

# Compare with previous best k on test data (from b)
test_accuracies = []

for k in k_values:
    knn = KNeighborsClassifier(n_neighbors=k)
    knn.fit(samples_train_polar, labels_train)
    test_pred = knn.predict(samples_test_polar)
    test_accuracies.append(calculate_accuracy(labels_test, test_pred))

best_k_test = k_values[np.argmax(test_accuracies)]
print(f"The best k value based on test data (from part b) is: {best_k_test}")
print(
    f"Test accuracy with best k from test data (k={best_k_test}): {max(test_accuracies):.4f}"
)

# Plot comparison
plt.figure(figsize=(12, 6))
plt.plot(
    k_values,
    cv_scores_mean,
    color=color1,
    linestyle="-",
    label="Cross-Validation Accuracy",
)
plt.fill_between(
    k_values,
    np.array(cv_scores_mean) - np.array(cv_scores_std),
    np.array(cv_scores_mean) + np.array(cv_scores_std),
    color=color1,
    alpha=0.2,
)
plt.plot(
    k_values,
    test_accuracies,
    color=color2,
    linestyle="-",
    label="Test Accuracy",
)
plt.axvline(
    x=best_k_cv,
    color=color1,
    linestyle="--",
    label=f"Best k (CV): {best_k_cv}",
)
plt.axvline(
    x=best_k_test,
    color=color2,
    linestyle="--",
    label=f"Best k (Test): {best_k_test}",
)
plt.xlabel("k (Number of Neighbors)")
plt.ylabel("Accuracy")
plt.title("Comparison of Cross-Validation and Test Accuracies")
plt.legend()
plt.grid(True)
plt.show()

# Plot k vs Cross-Validation Accuracy with error bars
plt.figure(figsize=(12, 6))
plt.errorbar(
    k_values,
    cv_scores_mean,
    yerr=cv_scores_std,
    fmt="o-",
    capsize=5,
    color=color1,
    ecolor=color2,
)
plt.xlabel("k (Number of Neighbors)")
plt.ylabel("Cross-Validation Accuracy")
plt.title(f"{n_splits}-Fold Cross-Validation Accuracy for KNN Classifier")
plt.grid(True)
plt.show()
