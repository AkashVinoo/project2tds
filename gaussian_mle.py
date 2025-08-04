import numpy as np

# Set the random number generator with the given seed
rng = np.random.default_rng(seed=1001)

# Define the Gaussian distribution parameters
mu_true = 3      # true mean
sigma_true = 1.5 # true standard deviation
n = 1000         # number of samples

print(f"Generating {n} samples from N(μ={mu_true}, σ²={sigma_true}²)")

# Generate 1000 points from the Gaussian distribution
X = rng.normal(loc=mu_true, scale=sigma_true, size=n)

print(f"Dataset generated successfully!")
print(f"Dataset size: {len(X)}")
print(f"First 10 samples: {X[:10]}")
print(f"Sample statistics:")
print(f"  Sample mean: {np.mean(X):.6f}")
print(f"  Sample std: {np.std(X):.6f}")
print(f"  True mean: {mu_true}")
print(f"  True std: {sigma_true}")

# For a Gaussian distribution N(μ, σ²), the likelihood function is:
# L(μ, σ²) = ∏(i=1 to n) (1/(σ√(2π))) * exp(-((x_i - μ)²)/(2σ²))

# Taking the log-likelihood:
# log L(μ, σ²) = -n/2 * log(2π) - n/2 * log(σ²) - (1/(2σ²)) * Σ(x_i - μ)²

# To find the MLE of μ, we take the derivative with respect to μ and set to 0:
# d/dμ [log L] = (1/σ²) * Σ(x_i - μ) = 0
# This gives us: Σ(x_i - μ) = 0
# Therefore: Σx_i = nμ
# So: μ = (1/n) * Σx_i = sample mean

# Therefore, the MLE of the mean is the sample mean
mle_mean = np.mean(X)

print(f"\nMLE calculation:")
print(f"  MLE of μ = (1/n) * Σx_i = sample mean")
print(f"  MLE of μ = {mle_mean:.6f}")

# Let's also verify this manually
manual_mle = np.sum(X) / len(X)
print(f"  Manual calculation: Σx_i/n = {np.sum(X)}/{len(X)} = {manual_mle:.6f}")

# Compare with true parameter
print(f"\nComparison:")
print(f"  True mean: {mu_true}")
print(f"  MLE estimate: {mle_mean:.6f}")
print(f"  Difference: {abs(mle_mean - mu_true):.6f}")

# Let's also calculate the MLE of variance for completeness
# The MLE of σ² is: σ²_hat = (1/n) * Σ(x_i - μ_hat)²
mle_variance = np.mean((X - mle_mean) ** 2)
mle_std = np.sqrt(mle_variance)

print(f"\nAdditional MLE calculations:")
print(f"  MLE of σ² = (1/n) * Σ(x_i - μ_hat)² = {mle_variance:.6f}")
print(f"  MLE of σ = √(MLE of σ²) = {mle_std:.6f}")
print(f"  True σ² = {sigma_true**2}")
print(f"  True σ = {sigma_true}")

print(f"\nAnswer: {mle_mean:.3f}") 