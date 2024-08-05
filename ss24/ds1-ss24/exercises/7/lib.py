import numpy as np


# src: https://stackoverflow.com/a/26757297
def cartesian_to_polar(x, y):
    r = np.sqrt(x**2 + y**2)
    theta = np.arctan2(y, x)
    # return r, theta
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
