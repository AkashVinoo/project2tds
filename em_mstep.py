import numpy as np
from scipy.stats import norm

def init():
    """
    Initialize the parameters of the GMM and return theta_0.
    """
    K = 3
    means = np.array([1.0, 2.0, 3.0])
    variances = np.array([1.0, 1.0, 1.0])
    pi = np.array([1/3, 1/3, 1/3])
    theta_0 = np.concatenate([means, variances, pi])
    return theta_0

def estep(theta, X):
    """
    Perform the E-step of the EM algorithm.
    """
    n = len(X)
    K = 3
    
    means = theta[:K]
    variances = theta[K:2*K]
    pi = theta[2*K:]
    
    lamb = np.zeros((n, K))
    
    for i in range(n):
        x_i = X[i]
        numerators = np.zeros(K)
        
        for k in range(K):
            mu_k = means[k]
            sigma2_k = variances[k]
            likelihood = norm.pdf(x_i, loc=mu_k, scale=np.sqrt(sigma2_k))
            numerators[k] = pi[k] * likelihood
        
        denominator = np.sum(numerators)
        
        if denominator > 0:
            for k in range(K):
                lamb[i, k] = numerators[k] / denominator
        else:
            for k in range(K):
                lamb[i, k] = 1.0 / K
    
    return lamb

def mstep(lamb, X):
    """
    Perform the M-step of the EM algorithm.
    
    Args:
        lamb: Responsibility matrix of shape (n, K) where lamb[i][k] = λik
        X: Data array of shape (n,)
    
    Returns:
        theta: Updated parameter vector of shape (3K,) containing [means, variances, pi]
    """
    n = len(X)
    K = lamb.shape[1]
    
    # Initialize updated parameters
    means_new = np.zeros(K)
    variances_new = np.zeros(K)
    pi_new = np.zeros(K)
    
    # Update mixture probabilities: πk = (1/n) * Σi λik
    for k in range(K):
        pi_new[k] = np.sum(lamb[:, k]) / n
    
    # Update means: μk = (Σi λik * xi) / (Σi λik)
    for k in range(K):
        numerator = np.sum(lamb[:, k] * X)
        denominator = np.sum(lamb[:, k])
        
        if denominator > 0:
            means_new[k] = numerator / denominator
        else:
            means_new[k] = 0.0  # Default value if no responsibility
    
    # Update variances: σ²k = (Σi λik * (xi - μk)²) / (Σi λik)
    for k in range(K):
        numerator = np.sum(lamb[:, k] * (X - means_new[k])**2)
        denominator = np.sum(lamb[:, k])
        
        if denominator > 0:
            variances_new[k] = numerator / denominator
        else:
            variances_new[k] = 1.0  # Default value if no responsibility
    
    # Combine parameters into theta
    theta = np.concatenate([means_new, variances_new, pi_new])
    
    return theta

def generate_gmm_data():
    """Generate the same dataset X as used in the previous problem."""
    rng = np.random.default_rng(seed=1001)
    
    pi = [0.3, 0.5, 0.2]
    means = [-4, 0, 5]
    variances = [2, 1, 3]
    std_devs = [np.sqrt(v) for v in variances]
    
    n_samples = 100000
    X = np.zeros(n_samples)
    
    for i in range(n_samples):
        k = rng.choice([0, 1, 2], p=pi)
        x = rng.normal(loc=means[k], scale=std_devs[k])
        X[i] = x
    
    return X

# Test the M-step function
if __name__ == "__main__":
    # Get theta_0, X, and lamb_1
    theta_0 = init()
    X = generate_gmm_data()
    lamb_1 = estep(theta_0, X)
    
    print("M-step Test:")
    print("=" * 40)
    print(f"Theta_0: {theta_0}")
    print(f"Lamb_1 shape: {lamb_1.shape}")
    
    # Perform M-step
    theta_1 = mstep(lamb_1, X)
    
    print(f"\nTheta_1: {theta_1}")
    
    # Extract parameters from theta_1
    K = 3
    means_1 = theta_1[:K]
    variances_1 = theta_1[K:2*K]
    pi_1 = theta_1[2*K:]
    
    print(f"\nUpdated Parameters:")
    print("Means (μ):")
    for i in range(K):
        print(f"  μ{i} = {means_1[i]:.6f}")
    
    print("\nVariances (σ²):")
    for i in range(K):
        print(f"  σ²{i} = {variances_1[i]:.6f}")
    
    print("\nMixture Probabilities (π):")
    for i in range(K):
        print(f"  π{i} = {pi_1[i]:.6f}")
    
    # Calculate norm of theta_1
    theta_1_norm = np.linalg.norm(theta_1)
    print(f"\n||θ(1)|| = {theta_1_norm:.6f}")
    
    # Compare with theta_0
    theta_0_norm = np.linalg.norm(theta_0)
    print(f"||θ(0)|| = {theta_0_norm:.6f}")
    print(f"Change in norm: {abs(theta_1_norm - theta_0_norm):.6f}")
    
    # Verify properties
    print(f"\nVerification:")
    print(f"  Sum of mixture probabilities: {np.sum(pi_1):.6f} (should be 1.0)")
    print(f"  All variances positive: {np.all(variances_1 > 0)}")
    
    print(f"\nAnswer: ||θ(1)|| = {theta_1_norm:.2f}") 