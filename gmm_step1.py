import numpy as np

# Set the random number generator with the given seed
rng = np.random.default_rng(seed=1001)

# Define the GMM parameters
# K = 3 mixtures, indexed from 0 to 2
# Mixture probabilities (π0, π1, π2)
pi = [0.3, 0.5, 0.2]

print("GMM with K=3 mixtures")
print("Mixture probabilities:")
for i, p in enumerate(pi):
    print(f"  π{i} = {p}")
print(f"Sum of probabilities: {sum(pi)}")

# Step 1: Choose one of the three mixtures based on the distribution
# This is equivalent to sampling from a categorical distribution with parameters π
k = rng.choice([0, 1, 2], p=pi)

print(f"\nStep 1: Choosing mixture component")
print(f"  Sampled mixture index k = {k}")
print(f"  This corresponds to mixture {k} with probability π{k} = {pi[k]}")

# Let's also verify the sampling by doing it multiple times to see the distribution
print(f"\nVerification: Sampling 1000 times to see the distribution:")
samples = rng.choice([0, 1, 2], p=pi, size=1000)
unique, counts = np.unique(samples, return_counts=True)
sample_dist = dict(zip(unique, counts))

print("Observed frequencies:")
for i in range(3):
    count = sample_dist.get(i, 0)
    freq = count / 1000
    print(f"  Mixture {i}: {count} times ({freq:.3f}) - Expected: {pi[i]:.3f}")

print(f"\nAnswer: k = {k}") 