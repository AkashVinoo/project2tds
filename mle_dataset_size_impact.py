import numpy as np
import matplotlib.pyplot as plt

# Set the random number generator with the given seed
rng = np.random.default_rng(seed=1001)

# Define the dataset sizes and true parameter
dataset_sizes = [10, 100, 1000, 10000, 100000, 1000000]
true_p = 0.2

# Lists to store results
mle_values = []
differences = []

print("Analyzing impact of dataset size on MLE...")
print("=" * 50)

# Generate datasets and compute MLE for each size
for n in dataset_sizes:
    print(f"\nProcessing dataset with n = {n:,}")
    
    # Sample from Bernoulli distribution with p=0.2
    X = rng.binomial(n=1, p=true_p, size=n)
    
    # Compute MLE (sample mean)
    mle_p = np.mean(X)
    
    # Compute absolute difference
    diff = abs(mle_p - true_p)
    
    # Store results
    mle_values.append(mle_p)
    differences.append(diff)
    
    # Print results
    print(f"  Number of 1s: {np.sum(X):,}")
    print(f"  MLE estimate: {mle_p:.6f}")
    print(f"  True parameter: {true_p:.6f}")
    print(f"  Difference |MLE - p|: {diff:.6f}")

# Create the plot
plt.figure(figsize=(12, 8))

# Plot 1: Linear scale
plt.subplot(2, 2, 1)
plt.plot(dataset_sizes, differences, 'bo-', linewidth=2, markersize=8)
plt.xlabel('Dataset Size (n)')
plt.ylabel('|MLE - p|')
plt.title('Impact of Dataset Size on MLE Accuracy (Linear Scale)')
plt.grid(True, alpha=0.3)
plt.xscale('linear')
plt.yscale('linear')

# Plot 2: Log-log scale
plt.subplot(2, 2, 2)
plt.loglog(dataset_sizes, differences, 'ro-', linewidth=2, markersize=8)
plt.xlabel('Dataset Size (n)')
plt.ylabel('|MLE - p|')
plt.title('Impact of Dataset Size on MLE Accuracy (Log-Log Scale)')
plt.grid(True, alpha=0.3)

# Plot 3: MLE values vs dataset size
plt.subplot(2, 2, 3)
plt.semilogx(dataset_sizes, mle_values, 'go-', linewidth=2, markersize=8, label='MLE estimate')
plt.axhline(y=true_p, color='red', linestyle='--', label=f'True parameter p={true_p}')
plt.xlabel('Dataset Size (n)')
plt.ylabel('MLE Estimate')
plt.title('MLE Estimates vs Dataset Size')
plt.legend()
plt.grid(True, alpha=0.3)

# Plot 4: Theoretical relationship (1/sqrt(n))
plt.subplot(2, 2, 4)
theoretical_error = 1 / np.sqrt(np.array(dataset_sizes))
plt.loglog(dataset_sizes, differences, 'bo-', linewidth=2, markersize=8, label='Observed error')
plt.loglog(dataset_sizes, theoretical_error, 'r--', linewidth=2, label='Theoretical: 1/√n')
plt.xlabel('Dataset Size (n)')
plt.ylabel('|MLE - p|')
plt.title('Observed vs Theoretical Error')
plt.legend()
plt.grid(True, alpha=0.3)

plt.tight_layout()
plt.show()

# Print summary table
print("\n" + "=" * 60)
print("SUMMARY TABLE")
print("=" * 60)
print(f"{'Dataset Size':<12} {'MLE Estimate':<15} {'True p':<10} {'|MLE - p|':<15}")
print("-" * 60)
for i, n in enumerate(dataset_sizes):
    print(f"{n:<12,} {mle_values[i]:<15.6f} {true_p:<10.6f} {differences[i]:<15.6f}")

# Analysis of the relationship
print("\n" + "=" * 60)
print("ANALYSIS")
print("=" * 60)

# Check if the relationship follows 1/sqrt(n)
print("Theoretical relationship: |MLE - p| ∝ 1/√n")
print("This means the error should decrease as the square root of the sample size increases.")

# Calculate the ratio of consecutive differences
print("\nRatio of consecutive differences (should be approximately √10 ≈ 3.16):")
for i in range(len(differences)-1):
    ratio = differences[i] / differences[i+1]
    expected_ratio = np.sqrt(dataset_sizes[i+1] / dataset_sizes[i])
    print(f"  {dataset_sizes[i]:,} → {dataset_sizes[i+1]:,}: {ratio:.3f} (expected: {expected_ratio:.3f})")

print(f"\nKey Observations:")
print(f"1. As dataset size increases, the MLE estimate gets closer to the true parameter p={true_p}")
print(f"2. The error decreases approximately as 1/√n (following the Central Limit Theorem)")
print(f"3. With larger samples, we get more precise estimates of the true parameter")
print(f"4. The MLE is consistent - it converges to the true parameter as n → ∞") 