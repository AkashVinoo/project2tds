import numpy as np

# True parameters θ = [-4, 0, 5, 2, 1, 3, 0.3, 0.5, 0.2]
theta_true = np.array([-4.0, 0.0, 5.0, 2.0, 1.0, 3.0, 0.3, 0.5, 0.2])

# Converged parameters θ* from the EM algorithm
theta_star = np.array([-3.94585325, 0.02014348, 5.00488842, 2.06801305, 0.96390146, 3.0322972, 0.30548887, 0.49423046, 0.20028068])

# Calculate distance
diff = theta_star - theta_true
distance_to_true = np.linalg.norm(diff)

print("Distance Calculation:")
print("=" * 30)
print(f"True parameters θ: {theta_true}")
print(f"Converged parameters θ*: {theta_star}")
print(f"Difference vector (θ* - θ): {diff}")
print(f"\nDistance ||θ* - θ|| = {distance_to_true:.6f}")

# Break down by components
K = 3
means_diff = diff[:K]
variances_diff = diff[K:2*K]
pi_diff = diff[2*K:]

print(f"\nComponent-wise differences:")
print(f"Means differences: {means_diff}")
print(f"Variances differences: {variances_diff}")
print(f"Mixture probabilities differences: {pi_diff}")

print(f"\nAnswer: {distance_to_true:.2f}") 