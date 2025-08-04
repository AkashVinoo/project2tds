import numpy as np

def entropy(p):
    if p == 0 or p == 1:
        return 0.0
    return -p * np.log2(p) - (1 - p) * np.log2(1 - p)

def IG(E, El, Er, gamma):
    return E - (gamma * El + (1 - gamma) * Er)

# Parent node: 200 out of 1000 belong to class-1
p_parent = 200 / 1000
parent_entropy = entropy(p_parent)

# Left child: 100 out of 1000, 50 belong to class-1
n_left = 100
n_total = 1000
p_left = 50 / 100
left_entropy = entropy(p_left)

gamma = n_left / n_total
# Right child: 1000-100 = 900 points, 200-50 = 150 class-1
n_right = n_total - n_left
p_right = 150 / 900
right_entropy = entropy(p_right)

info_gain = IG(parent_entropy, left_entropy, right_entropy, gamma)
print(f"Information gain: {info_gain:.3f}") 