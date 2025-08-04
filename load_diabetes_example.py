from sklearn.datasets import load_diabetes
import numpy as np
import matplotlib.pyplot as plt

def shuffle_data(X, y):
    """Shuffle X and y in unison and return them."""
    assert len(X) == len(y)
    indices = np.arange(len(X))
    np.random.shuffle(indices)
    return X[indices], y[indices]

def train_test_split(X, y, test_size):
    """Split X and y into train and test sets according to test_size."""
    n = len(X)
    n_test = int(test_size * n)
    X_train, X_test = X[:-n_test], X[-n_test:]
    y_train, y_test = y[:-n_test], y[-n_test:]
    return X_train, X_test, y_train, y_test

def compute_weights(X, y):
    """Compute the closed-form solution for linear regression weights."""
    # X: (n_samples, n_features), y: (n_samples,)
    # w = (X^T X)^(-1) X^T y
    return np.linalg.inv(X.T @ X) @ X.T @ y

def MSE(X, y, w):
    """Compute mean squared error for given X, y, and weights w."""
    y_pred = X @ w
    return np.mean((y - y_pred) ** 2)

def compute_weights_ridge(X, y, alpha):
    """Compute the closed-form solution for Ridge regression weights."""
    n_features = X.shape[1]
    I = np.eye(n_features)
    return np.linalg.inv(X.T @ X + alpha * I) @ X.T @ y

X, y = load_diabetes(return_X_y=True)
np.random.seed(0)

print(f"Number of samples in the dataset: {X.shape[0]}")
print(f"Number of features in the dataset: {X.shape[1]}")

# Shuffle the data
X_shuffled, y_shuffled = shuffle_data(X, y)

# Mean of the first 5 values in y after shuffling
y_first5_mean = np.mean(y_shuffled[:5])
print(f"Mean of the first 5 values in shuffled y: {y_first5_mean}")

# Split the data with test_size=0.25
X_train, X_test, y_train, y_test = train_test_split(X_shuffled, y_shuffled, test_size=0.25)
print(f"Sum of all y values in y_test: {np.sum(y_test)}")

print(f"Shapes: X_train: {X_train.shape}, X_test: {X_test.shape}, y_train: {y_train.shape}, y_test: {y_test.shape}")

# Add a dummy feature (column of 1's as the first column) to X_train and X_test
X_train_dummy = np.hstack([np.ones((X_train.shape[0], 1)), X_train])
X_test_dummy = np.hstack([np.ones((X_test.shape[0], 1)), X_test])

# Take the transpose
X_train_T = X_train_dummy.T
X_test_T = X_test_dummy.T

print(f"Shapes after adding dummy feature and transpose: X_train: {X_train_T.shape}, X_test: {X_test_T.shape}")

# Compute weights using closed-form linear regression
weights = compute_weights(X_train_dummy, y_train)
print(f"Intercept (rounded to 1 decimal place): {round(weights[0], 1)}")

# Compute train and test error
train_error = MSE(X_train_dummy, y_train, weights)
test_error = MSE(X_test_dummy, y_test, weights)
print(f"Train error (MSE): {train_error}")
print(f"Test error (MSE): {test_error}")

# Compute Ridge regression weights
ridge_weights = compute_weights_ridge(X_train_dummy, y_train, 0.3)
print(f"Sum of Ridge weights: {np.sum(ridge_weights)}")
print(f"Reduction in sum of weights compared to plain regression: {np.sum(weights) - np.sum(ridge_weights)}")

# Compute Ridge regression train and test error
ridge_train_error = MSE(X_train_dummy, y_train, ridge_weights)
ridge_test_error = MSE(X_test_dummy, y_test, ridge_weights)
print(f"Ridge train error (MSE): {ridge_train_error}")
print(f"Ridge test error (MSE): {ridge_test_error}")
print(f"Absolute difference between Ridge train and test error: {abs(ridge_train_error - ridge_test_error)}")

# Ridge regularization strengths
alphas = np.linspace(0, 5, 10)
sums_of_weights = []

for alpha in alphas:
    w = compute_weights_ridge(X_train_dummy, y_train, alpha)
    sums_of_weights.append(np.sum(w))

plt.figure()
plt.plot(alphas, sums_of_weights, marker='o')
plt.xlabel('Regularization strength (alpha)')
plt.ylabel('Sum of Ridge weights')
plt.title('Sum of Ridge weights vs Regularization strength')
plt.grid(True)
plt.show() 