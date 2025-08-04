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
    
    Args:
        X: Data array
        theta_0: Initial parameter vector
        tolerance: Stopping criterion threshold
        max_iterations: Maximum number of iterations
    
    Returns:
        theta_final: Final parameter vector
        num_iterations: Number of iterations performed
        convergence_history: List of distances at each iteration
    """
    theta_t = theta_0.copy()
    convergence_history = []
    
    print("EM Algorithm Progress:")
    print("=" * 50)
    
    for iteration in range(max_iterations):
        # E-step
        lamb = estep(theta_t, X)
        
        # M-step
        theta_t_plus_1 = mstep(lamb, X)
        
        # Calculate distance
        dist = distance(theta_t, theta_t_plus_1)
        convergence_history.append(dist)
        
        # Print progress every 10 iterations
        if iteration % 10 == 0 or iteration < 5:
            print(f"Iteration {iteration:3d}: Distance = {dist:.6f}")
        
        # Check convergence
        if dist < tolerance:
            print(f"\nConverged at iteration {iteration}!")
            print(f"Final distance: {dist:.6f}")
            return theta_t_plus_1, iteration + 1, convergence_history
        
        # Update for next iteration
        theta_t = theta_t_plus_1
    
    print(f"\nDid not converge within {max_iterations} iterations!")
    return theta_t, max_iterations, convergence_history

# Run the complete EM algorithm
if __name__ == "__main__":
    # Get data and initial parameters
    X = generate_gmm_data()
    theta_0 = init()
    
    print("EM Algorithm with Stopping Criterion")
    print("=" * 50)
    print(f"Dataset size: {len(X)}")
    print(f"Initial parameters: {theta_0}")
    print(f"Stopping criterion: ||θ(t+1) - θ(t)|| < 0.01")
    
    # Run EM algorithm
    theta_final, num_iterations, convergence_history = em_algorithm(X, theta_0, tolerance=0.01)
    
    print(f"\nResults:")
    print(f"Number of iterations: {num_iterations}")
    print(f"Final parameters: {theta_final}")
    
    # Extract final parameters
    K = 3
    means_final = theta_final[:K]
    variances_final = theta_final[K:2*K]
    pi_final = theta_final[2*K:]
    
    print(f"\nFinal GMM Parameters:")
    print("Means (μ):")
    for i in range(K):
        print(f"  μ{i} = {means_final[i]:.6f}")
    
    print("\nVariances (σ²):")
    for i in range(K):
        print(f"  σ²{i} = {variances_final[i]:.6f}")
    
    print("\nMixture Probabilities (π):")
    for i in range(K):
        print(f"  π{i} = {pi_final[i]:.6f}")
    
    # Compare with true parameters
    true_means = [-4, 0, 5]
    true_variances = [2, 1, 3]
    true_pi = [0.3, 0.5, 0.2]
    
    print(f"\nComparison with True Parameters:")
    print("Means:")
    for i in range(K):
        print(f"  True μ{i} = {true_means[i]}, Estimated μ{i} = {means_final[i]:.6f}")
    
    print("\nVariances:")
    for i in range(K):
        print(f"  True σ²{i} = {true_variances[i]}, Estimated σ²{i} = {variances_final[i]:.6f}")
    
    print("\nMixture Probabilities:")
    for i in range(K):
        print(f"  True π{i} = {true_pi[i]}, Estimated π{i} = {pi_final[i]:.6f}")
    
    # Plot convergence history
    try:
        import matplotlib.pyplot as plt
        
        plt.figure(figsize=(10, 6))
        plt.plot(convergence_history, 'b-', linewidth=2)
        plt.axhline(y=0.01, color='r', linestyle='--', label='Tolerance (0.01)')
        plt.xlabel('Iteration')
        plt.ylabel('Distance ||θ(t+1) - θ(t)||')
        plt.title('EM Algorithm Convergence')
        plt.legend()
        plt.grid(True, alpha=0.3)
        plt.yscale('log')
        plt.show()
        
    except ImportError:
        print("\nMatplotlib not available for plotting")
    
    print(f"\nAnswer: {num_iterations}") 