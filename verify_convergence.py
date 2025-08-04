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
    """
    diff = theta_t_plus_1 - theta_t
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

def em_algorithm(X, theta_0, tolerance=0.01, max_iterations=1000):
    """
    Run the EM algorithm until convergence.
    """
    theta_t = theta_0.copy()
    convergence_history = []
    
    for iteration in range(max_iterations):
        # E-step
        lamb = estep(theta_t, X)
        
        # M-step
        theta_t_plus_1 = mstep(lamb, X)
        
        # Calculate distance
        dist = distance(theta_t, theta_t_plus_1)
        convergence_history.append(dist)
        
        # Check convergence
        if dist < tolerance:
            return theta_t_plus_1, iteration + 1, convergence_history
        
        # Update for next iteration
        theta_t = theta_t_plus_1
    
    return theta_t, max_iterations, convergence_history

# Calculate distance between converged and true parameters
if __name__ == "__main__":
    # Get data and run EM algorithm
    X = generate_gmm_data()
    theta_0 = init()
    theta_star, num_iterations, _ = em_algorithm(X, theta_0, tolerance=0.01)
    
    # Define true parameters
    # θ = [-4, 0, 5, 2, 1, 3, 0.3, 0.5, 0.2]
    theta_true = np.array([-4.0, 0.0, 5.0, 2.0, 1.0, 3.0, 0.3, 0.5, 0.2])
    
    print("Verification of EM Algorithm Convergence")
    print("=" * 50)
    print(f"Number of iterations to converge: {num_iterations}")
    
    print(f"\nTrue parameters θ:")
    print(f"  Means: {theta_true[:3]}")
    print(f"  Variances: {theta_true[3:6]}")
    print(f"  Mixture probabilities: {theta_true[6:]}")
    
    print(f"\nConverged parameters θ*:")
    print(f"  Means: {theta_star[:3]}")
    print(f"  Variances: {theta_star[3:6]}")
    print(f"  Mixture probabilities: {theta_star[6:]}")
    
    # Calculate distance between θ* and θ
    diff = theta_star - theta_true
    distance_to_true = np.linalg.norm(diff)
    
    print(f"\nDifference vector (θ* - θ): {diff}")
    
    # Break down the differences by component
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
    
    # Calculate individual component distances
    means_distance = np.linalg.norm(means_diff)
    variances_distance = np.linalg.norm(variances_diff)
    pi_distance = np.linalg.norm(pi_diff)
    
    print(f"\nComponent-wise distances:")
    print(f"  Means distance: {means_distance:.6f}")
    print(f"  Variances distance: {variances_distance:.6f}")
    print(f"  Mixture probabilities distance: {pi_distance:.6f}")
    
    # Verify the calculation manually
    manual_distance = np.sqrt(np.sum(diff**2))
    print(f"\nManual calculation:")
    print(f"  √(Σ(θ* - θ)²) = {manual_distance:.6f}")
    print(f"  Matches function result: {np.isclose(distance_to_true, manual_distance)}")
    
    # Calculate relative errors
    print(f"\nRelative errors:")
    for i in range(K):
        rel_error_mean = abs(means_diff[i] / theta_true[i]) * 100
        print(f"  μ{i} relative error: {rel_error_mean:.2f}%")
    
    for i in range(K):
        rel_error_var = abs(variances_diff[i] / theta_true[i+3]) * 100
        print(f"  σ²{i} relative error: {rel_error_var:.2f}%")
    
    for i in range(K):
        rel_error_pi = abs(pi_diff[i] / theta_true[i+6]) * 100
        print(f"  π{i} relative error: {rel_error_pi:.2f}%")
    
    print(f"\nAnswer: ||θ* - θ|| = {distance_to_true:.2f}") 