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
    """
    n = len(X)
    K = lamb.shape[1]
    
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
            means_new[k] = 0.0
    
    # Update variances: σ²k = (Σi λik * (xi - μk)²) / (Σi λik)
    for k in range(K):
        numerator = np.sum(lamb[:, k] * (X - means_new[k])**2)
        denominator = np.sum(lamb[:, k])
        
        if denominator > 0:
            variances_new[k] = numerator / denominator
        else:
            variances_new[k] = 1.0
    
    theta = np.concatenate([means_new, variances_new, pi_new])
    return theta

def distance(theta_t, theta_t_plus_1):
    """
    Calculate the distance between two parameter vectors.
    
    Args:
        theta_t: Parameter vector at iteration t
        theta_t_plus_1: Parameter vector at iteration t+1
    
    Returns:
        distance: ||θ(t+1) - θ(t)||
    """
    # Calculate the difference vector
    diff = theta_t_plus_1 - theta_t
    
    # Calculate the norm of the difference
    dist = np.linalg.norm(diff)
    
    return dist

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

# Test the distance function
if __name__ == "__main__":
    # Get theta_0, X, and theta_1
    theta_0 = init()
    X = generate_gmm_data()
    lamb_1 = estep(theta_0, X)
    theta_1 = mstep(lamb_1, X)
    
    print("Distance Function Test:")
    print("=" * 40)
    print(f"Theta_0: {theta_0}")
    print(f"Theta_1: {theta_1}")
    
    # Calculate distance between theta_0 and theta_1
    dist = distance(theta_0, theta_1)
    
    print(f"\nDistance calculation:")
    print(f"  ||θ(1) - θ(0)|| = {dist:.6f}")
    
    # Let's also break down the calculation
    diff = theta_1 - theta_0
    print(f"\nDifference vector (θ(1) - θ(0)): {diff}")
    
    # Calculate individual component differences
    K = 3
    means_diff = diff[:K]
    variances_diff = diff[K:2*K]
    pi_diff = diff[2*K:]
    
    print(f"\nComponent-wise differences:")
    print("Means differences:")
    for i in range(K):
        print(f"  Δμ{i} = {means_diff[i]:.6f}")
    
    print("\nVariances differences:")
    for i in range(K):
        print(f"  Δσ²{i} = {variances_diff[i]:.6f}")
    
    print("\nMixture probabilities differences:")
    for i in range(K):
        print(f"  Δπ{i} = {pi_diff[i]:.6f}")
    
    # Verify the calculation manually
    manual_dist = np.sqrt(np.sum(diff**2))
    print(f"\nManual calculation:")
    print(f"  √(Σ(θ(1) - θ(0))²) = {manual_dist:.6f}")
    print(f"  Matches function result: {np.isclose(dist, manual_dist)}")
    
    # Compare with individual norms
    norm_theta_0 = np.linalg.norm(theta_0)
    norm_theta_1 = np.linalg.norm(theta_1)
    print(f"\nIndividual norms:")
    print(f"  ||θ(0)|| = {norm_theta_0:.6f}")
    print(f"  ||θ(1)|| = {norm_theta_1:.6f}")
    print(f"  | ||θ(1)|| - ||θ(0)|| | = {abs(norm_theta_1 - norm_theta_0):.6f}")
    
    print(f"\nAnswer: {dist:.2f}") 