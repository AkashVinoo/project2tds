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
    
    Args:
        theta: Parameter vector of shape (3K,) containing [means, variances, pi]
        X: Data array of shape (n,)
    
    Returns:
        lamb: Responsibility matrix of shape (n, K) where lamb[i][k] = λik
    """
    n = len(X)
    K = 3
    
    # Extract parameters from theta
    means = theta[:K]
    variances = theta[K:2*K]
    pi = theta[2*K:]
    
    # Initialize responsibility matrix
    lamb = np.zeros((n, K))
    
    # For each data point
    for i in range(n):
        x_i = X[i]
        
        # Calculate the numerator for each mixture k
        numerators = np.zeros(K)
        for k in range(K):
            # Calculate the Gaussian probability density
            # P(x_i | k) = (1/sqrt(2πσ²_k)) * exp(-(x_i - μ_k)²/(2σ²_k))
            mu_k = means[k]
            sigma2_k = variances[k]
            
            # Using scipy.stats.norm.pdf for numerical stability
            likelihood = norm.pdf(x_i, loc=mu_k, scale=np.sqrt(sigma2_k))
            
            # Multiply by mixture probability
            numerators[k] = pi[k] * likelihood
        
        # Calculate the denominator (total probability)
        denominator = np.sum(numerators)
        
        # Avoid division by zero
        if denominator > 0:
            # Calculate responsibilities
            for k in range(K):
                lamb[i, k] = numerators[k] / denominator
        else:
            # If denominator is zero, assign equal responsibilities
            lamb[i, k] = 1.0 / K
    
    return lamb

# Generate the dataset X from the previous GMM sampling
def generate_gmm_data():
    """Generate the same dataset X as used in the previous problem."""
    rng = np.random.default_rng(seed=1001)
    
    # GMM parameters
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

# Test the E-step function
if __name__ == "__main__":
    # Get theta_0 and X
    theta_0 = init()
    X = generate_gmm_data()
    
    print("E-step Test:")
    print("=" * 40)
    print(f"Theta_0: {theta_0}")
    print(f"X shape: {X.shape}")
    print(f"First 10 values of X: {X[:10]}")
    
    # Perform E-step
    lamb_1 = estep(theta_0, X)
    
    print(f"\nLamb_1 shape: {lamb_1.shape}")
    print(f"First few rows of lamb_1:")
    print(lamb_1[:5])
    
    # Calculate sum of zeroth column
    sum_zeroth_column = np.sum(lamb_1[:, 0])
    print(f"\nSum of zeroth column: {sum_zeroth_column:.6f}")
    
    # Verify properties of responsibility matrix
    print(f"\nVerification:")
    print(f"  Sum of responsibilities for each row should be 1:")
    row_sums = np.sum(lamb_1, axis=1)
    print(f"  Min row sum: {np.min(row_sums):.6f}")
    print(f"  Max row sum: {np.max(row_sums):.6f}")
    print(f"  Mean row sum: {np.mean(row_sums):.6f}")
    
    # Check column sums (should be approximately n * π_k)
    print(f"\nColumn sums (should be approximately n * π_k):")
    for k in range(3):
        col_sum = np.sum(lamb_1[:, k])
        expected = len(X) * theta_0[6+k]  # pi[k]
        print(f"  Column {k}: {col_sum:.2f} (expected: {expected:.2f})")
    
    print(f"\nAnswer: {sum_zeroth_column:.2f}") 