import numpy as np

# Set the random number generator with the given seed
rng = np.random.default_rng(seed=1001)

# From the previous question, we obtained k = 1
k = 1

# Define the GMM parameters
# Mixture probabilities (π0, π1, π2)
pi = [0.3, 0.5, 0.2]

# Means and variances of the mixtures
# Note: The problem gives μ1, μ2, μ3 but we're using 0-indexing, so:
# μ1 corresponds to mixture 0, μ2 to mixture 1, μ3 to mixture 2
means = [-4, 0, 5]      # μ1, μ2, μ3
variances = [2, 1, 3]   # σ²1, σ²2, σ²3
std_devs = [np.sqrt(v) for v in variances]  # σ1, σ2, σ3

print("GMM Parameters:")
print("Mixture probabilities:")
for i, p in enumerate(pi):
    print(f"  π{i} = {p}")
print("\nMixture parameters:")
for i in range(3):
    print(f"  Mixture {i}: μ{i+1} = {means[i]}, σ²{i+1} = {variances[i]}, σ{i+1} = {std_devs[i]:.3f}")

print(f"\nFrom previous step: k = {k}")
print(f"This corresponds to mixture {k} with parameters:")
print(f"  μ{k+1} = {means[k]}")
print(f"  σ²{k+1} = {variances[k]}")
print(f"  σ{k+1} = {std_devs[k]:.3f}")

# Step 2: Sample a point from mixture k
# We sample from N(μk, σ²k)
x = rng.normal(loc=means[k], scale=std_devs[k])

print(f"\nStep 2: Sampling from mixture {k}")
print(f"  Sampling from N(μ{k+1}={means[k]}, σ²{k+1}={variances[k]})")
print(f"  Sampled point x = {x:.6f}")

# Let's also verify by sampling multiple points to see the distribution
print(f"\nVerification: Sampling 1000 points from mixture {k}:")
samples = rng.normal(loc=means[k], scale=std_devs[k], size=1000)
print(f"  Sample mean: {np.mean(samples):.3f} (expected: {means[k]})")
print(f"  Sample variance: {np.var(samples):.3f} (expected: {variances[k]})")
print(f"  Sample std: {np.std(samples):.3f} (expected: {std_devs[k]:.3f})")

print(f"\nAnswer: {x:.3f}") 