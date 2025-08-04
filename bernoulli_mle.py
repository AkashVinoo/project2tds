import numpy as np

# Set the seed and generate the data
rng = np.random.default_rng(seed=1001)
X = rng.integers(0, 2, size=1000)

print("Dataset X (first 20 values):", X[:20])
print("Dataset size:", len(X))
print("Number of 1s:", np.sum(X))
print("Number of 0s:", len(X) - np.sum(X))

# For a Bernoulli distribution with parameter p:
# - P(X=1) = p
# - P(X=0) = 1-p

# The likelihood function is: L(p) = p^(sum of 1s) * (1-p)^(sum of 0s)
# Taking the log: log L(p) = (sum of 1s) * log(p) + (sum of 0s) * log(1-p)

# To find the MLE, we take the derivative with respect to p and set to 0:
# d/dp [log L(p)] = (sum of 1s)/p - (sum of 0s)/(1-p) = 0

# Solving: (sum of 1s)/p = (sum of 0s)/(1-p)
# (sum of 1s)(1-p) = (sum of 0s)p
# sum of 1s - (sum of 1s)p = (sum of 0s)p
# sum of 1s = (sum of 1s + sum of 0s)p
# sum of 1s = n*p
# p = (sum of 1s)/n

# Therefore, the MLE of p is the sample mean
mle_p = np.mean(X)

print(f"\nMaximum Likelihood Estimate of p (mean): {mle_p:.3f}")

# Verification: Let's also calculate it manually
sum_ones = np.sum(X)
n = len(X)
manual_mle = sum_ones / n
print(f"Manual calculation: {sum_ones}/{n} = {manual_mle:.3f}")

# The MLE of the mean for a Bernoulli distribution is simply the sample mean
# which is the proportion of 1s in the dataset
print(f"\nAnswer: {mle_p:.3f}") 