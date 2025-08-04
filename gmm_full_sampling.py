import numpy as np

# Set the random number generator with the given seed
rng = np.random.default_rng(seed=1001)

# Define the GMM parameters
# K = 3 mixtures, indexed from 0 to 2
pi = [0.3, 0.5, 0.2]  # Mixture probabilities

# Means and variances of the mixtures
# μ1, μ2, μ3 correspond to mixtures 0, 1, 2 respectively
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

# Initialize array to store samples
n_samples = 100000
X = np.zeros(n_samples)

print(f"\nSampling {n_samples:,} points from GMM...")

# Sample each point step by step
for i in range(n_samples):
    # Step 1: Choose mixture component k
    k = rng.choice([0, 1, 2], p=pi)
    
    # Step 2: Sample from the chosen mixture
    x = rng.normal(loc=means[k], scale=std_devs[k])
    
    # Store the sample
    X[i] = x

print(f"Sampling completed!")

# Calculate statistics
sample_mean = np.mean(X)
sample_std = np.std(X)
sample_var = np.var(X)

print(f"\nSample Statistics:")
print(f"  Sample mean: {sample_mean:.6f}")
print(f"  Sample std: {sample_std:.6f}")
print(f"  Sample variance: {sample_var:.6f}")

# Theoretical mean calculation
# E[X] = Σ πᵢ × μᵢ
theoretical_mean = sum(pi[i] * means[i] for i in range(3))
print(f"  Theoretical mean: {theoretical_mean:.6f}")

# Theoretical variance calculation
# Var[X] = Σ πᵢ × (σ²ᵢ + (μᵢ - E[X])²)
theoretical_var = sum(pi[i] * (variances[i] + (means[i] - theoretical_mean)**2) for i in range(3))
theoretical_std = np.sqrt(theoretical_var)
print(f"  Theoretical variance: {theoretical_var:.6f}")
print(f"  Theoretical std: {theoretical_std:.6f}")

# Let's also analyze the distribution of mixture assignments
print(f"\nMixture assignment analysis:")
# Count how many times each mixture was chosen
mixture_counts = np.zeros(3)
for i in range(n_samples):
    # We need to recreate the sampling to get the mixture assignments
    # For efficiency, let's do this separately
    pass

# Let's sample the mixture assignments separately for analysis
mixture_assignments = rng.choice([0, 1, 2], p=pi, size=n_samples)
unique, counts = np.unique(mixture_assignments, return_counts=True)
mixture_dist = dict(zip(unique, counts))

print("Observed mixture frequencies:")
for i in range(3):
    count = mixture_dist.get(i, 0)
    freq = count / n_samples
    print(f"  Mixture {i}: {count:,} times ({freq:.3f}) - Expected: {pi[i]:.3f}")

# Show first few samples
print(f"\nFirst 10 samples:")
for i in range(10):
    print(f"  X[{i}] = {X[i]:.6f}")

print(f"\nAnswer: {sample_mean:.3f}") 