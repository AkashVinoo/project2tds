import numpy as np

def init():
    """
    Initialize the parameters of the GMM and return theta_0.
    
    Returns:
        theta_0: NumPy array of shape (3K,) where:
            - First K elements: means of the three mixtures
            - Next K elements: variances of the three mixtures  
            - Last K elements: mixture probabilities
    """
    # GMM parameters for K=3
    K = 3
    
    # Initialize means: μ0=1, μ1=2, μ2=3
    means = np.array([1.0, 2.0, 3.0])
    
    # Initialize variances: σ²0=σ²1=σ²2=1
    variances = np.array([1.0, 1.0, 1.0])
    
    # Initialize mixture probabilities: π0=π1=π2=1/3
    pi = np.array([1/3, 1/3, 1/3])
    
    # Combine all parameters into theta_0
    # Order: [μ0, μ1, μ2, σ²0, σ²1, σ²2, π0, π1, π2]
    theta_0 = np.concatenate([means, variances, pi])
    
    return theta_0

# Test the initialization function
if __name__ == "__main__":
    theta_0 = init()
    
    print("GMM Initialization Parameters:")
    print("=" * 40)
    
    K = 3
    means = theta_0[:K]
    variances = theta_0[K:2*K]
    pi = theta_0[2*K:]
    
    print("Means (μ):")
    for i in range(K):
        print(f"  μ{i} = {means[i]}")
    
    print("\nVariances (σ²):")
    for i in range(K):
        print(f"  σ²{i} = {variances[i]}")
    
    print("\nMixture Probabilities (π):")
    for i in range(K):
        print(f"  π{i} = {pi[i]:.6f}")
    
    print(f"\nTheta_0 shape: {theta_0.shape}")
    print(f"Theta_0: {theta_0}")
    
    # Calculate the norm of theta_0
    theta_norm = np.linalg.norm(theta_0)
    print(f"\n||θ(0)|| = {theta_norm:.6f}")
    
    # Verify the structure
    print(f"\nVerification:")
    print(f"  Number of means: {len(means)}")
    print(f"  Number of variances: {len(variances)}")
    print(f"  Number of mixture probabilities: {len(pi)}")
    print(f"  Total parameters: {len(theta_0)}")
    print(f"  Sum of mixture probabilities: {np.sum(pi):.6f} (should be 1.0)")
    
    print(f"\nAnswer: ||θ(0)|| = {theta_norm:.2f}") 