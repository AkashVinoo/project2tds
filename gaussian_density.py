import numpy as np
from scipy.stats import norm

# Define the Gaussian distribution parameters
mu = 3      # mean
sigma = 1.5 # standard deviation
x = 5       # point at which we want to compute the density

print(f"Gaussian distribution: N(μ={mu}, σ²={sigma}²)")
print(f"Point of interest: x = {x}")

# Method 1: Using scipy.stats.norm.pdf
density_scipy = norm.pdf(x, loc=mu, scale=sigma)

# Method 2: Manual calculation using the PDF formula
# PDF of N(μ, σ²): f(x) = (1/(σ√(2π))) * exp(-((x-μ)²)/(2σ²))
def normal_pdf(x, mu, sigma):
    coefficient = 1 / (sigma * np.sqrt(2 * np.pi))
    exponent = -((x - mu) ** 2) / (2 * sigma ** 2)
    return coefficient * np.exp(exponent)

density_manual = normal_pdf(x, mu, sigma)

# Calculate components for detailed breakdown
coefficient = 1 / (sigma * np.sqrt(2 * np.pi))
exponent = -((x - mu) ** 2) / (2 * sigma ** 2)

print(f"\nCalculations:")
print(f"  Using scipy.stats.norm.pdf: {density_scipy:.6f}")
print(f"  Manual calculation: {density_manual:.6f}")

# Verify they are the same
print(f"  Are they equal? {np.isclose(density_scipy, density_manual)}")

# Let's break down the manual calculation
print(f"\nManual calculation breakdown:")
print(f"  μ = {mu}")
print(f"  σ = {sigma}")
print(f"  x = {x}")
print(f"  x - μ = {x} - {mu} = {x - mu}")
print(f"  (x - μ)² = ({x - mu})² = {(x - mu) ** 2}")
print(f"  2σ² = 2 × {sigma}² = 2 × {sigma ** 2} = {2 * sigma ** 2}")
print(f"  Exponent: -({(x - mu) ** 2})/({2 * sigma ** 2}) = {exponent:.6f}")
print(f"  exp(exponent) = {np.exp(exponent):.6f}")
print(f"  Coefficient: 1/({sigma} × √(2π)) = 1/({sigma * np.sqrt(2 * np.pi):.6f}) = {coefficient:.6f}")
print(f"  Final result: {coefficient:.6f} × {np.exp(exponent):.6f} = {density_manual:.6f}")

# Let's also plot the distribution to visualize
try:
    import matplotlib.pyplot as plt
    
    # Create a range of x values around the mean
    x_range = np.linspace(mu - 4*sigma, mu + 4*sigma, 1000)
    y_range = norm.pdf(x_range, loc=mu, scale=sigma)
    
    plt.figure(figsize=(10, 6))
    plt.plot(x_range, y_range, 'b-', linewidth=2, label=f'N({mu}, {sigma}²)')
    plt.axvline(x=mu, color='g', linestyle='--', label=f'Mean (μ={mu})')
    plt.axvline(x=x, color='r', linestyle='--', label=f'Point x={x}')
    plt.scatter([x], [density_scipy], color='red', s=100, zorder=5, label=f'Density at x={x}')
    
    plt.xlabel('x')
    plt.ylabel('Probability Density')
    plt.title(f'Gaussian Distribution N({mu}, {sigma}²)')
    plt.legend()
    plt.grid(True, alpha=0.3)
    plt.show()
    
except ImportError:
    print("\nMatplotlib not available for plotting")

print(f"\nAnswer: {density_scipy:.3f}") 