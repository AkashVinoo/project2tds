import numpy as np

# Data generation (DO NOT CHANGE)
rng = np.random.default_rng(seed=1001)
n_per = 50
cov = np.eye(2) / 10
X1 = rng.multivariate_normal([1, 1], cov, n_per)
y1 = np.ones(n_per)
X2 = rng.multivariate_normal([5, 3], cov, n_per)
y2 = np.zeros(n_per)
X3 = rng.multivariate_normal([3, 4], cov, n_per)
y3 = np.ones(n_per)
X4 = rng.multivariate_normal([3, 2], cov, n_per)
y4 = np.zeros(n_per)
X = np.concatenate((X1, X2, X3, X4), axis=0)
y = np.int64(np.concatenate((y1, y2, y3, y4)))

# Entropy function
def entropy(p):
    if p == 0 or p == 1:
        return 0.0
    return -p * np.log2(p) - (1 - p) * np.log2(1 - p)

def IG(E, El, Er, gamma):
    return E - (gamma * El + (1 - gamma) * Er)

def best_split(X, y):
    n, d = X.shape
    E_parent = entropy(np.mean(y))
    ig_best = -np.inf
    feat_best = None
    value_best = None
    for k in range(d):
        thresholds = np.unique(X[:, k])
        for theta in thresholds:
            left = y[X[:, k] < theta]
            right = y[X[:, k] >= theta]
            if len(left) == 0 or len(right) == 0:
                continue
            gamma = len(left) / n
            El = entropy(np.mean(left))
            Er = entropy(np.mean(right))
            ig = IG(E_parent, El, Er, gamma)
            if ig > ig_best:
                ig_best = ig
                feat_best = k
                value_best = theta
    return feat_best, value_best, ig_best

feat_best, value_best, ig_best = best_split(X, y)
print(f"Best feature index: {feat_best}")
print(f"Best threshold value: {value_best}")
print(f"Best information gain: {ig_best:.3f}") 