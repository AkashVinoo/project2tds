import numpy as np

# Set the random number generator with the given seed
rng = np.random.default_rng(seed=1001)

# Define the categorical distribution parameters
# Faces: 1, 2, 3, 4, 5, 6
# Parameters: [0.1, 0.2, 0.3, 0.3, 0.05, 0.05]
p_true = [0.1, 0.2, 0.3, 0.3, 0.05, 0.05]

print("True parameters for faces 1-6:", p_true)
print("Sum of probabilities:", sum(p_true))

# Sample 1000 points from the categorical distribution
# Using np.random.choice with the given probabilities
faces = [1, 2, 3, 4, 5, 6]
X = rng.choice(faces, size=1000, p=p_true)

print(f"\nDataset size: {len(X)}")
print("First 20 samples:", X[:20])

# Count the frequency of each face
unique, counts = np.unique(X, return_counts=True)
face_counts = dict(zip(unique, counts))

print("\nFrequency of each face:")
for face in faces:
    count = face_counts.get(face, 0)
    print(f"  Face {face}: {count} times")

# For a categorical distribution with parameters p = [p1, p2, p3, p4, p5, p6]:
# - P(X=1) = p1
# - P(X=2) = p2
# - P(X=3) = p3
# - P(X=4) = p4
# - P(X=5) = p5
# - P(X=6) = p6

# The likelihood function is: L(p) = p1^(count of 1s) * p2^(count of 2s) * ... * p6^(count of 6s)
# Taking the log: log L(p) = (count of 1s)*log(p1) + (count of 2s)*log(p2) + ... + (count of 6s)*log(p6)

# To find the MLE, we need to maximize this under the constraint that p1 + p2 + p3 + p4 + p5 + p6 = 1
# Using Lagrange multipliers, we get: p_i = (count of i)/n

# Therefore, the MLE of p3 is: p3_hat = (count of 3s)/n
count_3 = face_counts.get(3, 0)
n = len(X)
mle_p3 = count_3 / n

print(f"\nMLE calculation for p3:")
print(f"  Count of face 3: {count_3}")
print(f"  Total samples: {n}")
print(f"  MLE of p3: {count_3}/{n} = {mle_p3:.3f}")

# Let's also calculate MLE for all parameters for verification
mle_all = []
for face in faces:
    count = face_counts.get(face, 0)
    mle_p = count / n
    mle_all.append(mle_p)
    print(f"  MLE of p{face}: {count}/{n} = {mle_p:.3f}")

print(f"\nSum of MLE estimates: {sum(mle_all):.3f}")

# Compare with true parameters
print(f"\nComparison with true parameters:")
for i, face in enumerate(faces):
    true_p = p_true[i]
    mle_p = mle_all[i]
    diff = abs(mle_p - true_p)
    print(f"  Face {face}: True={true_p:.3f}, MLE={mle_p:.3f}, |Diff|={diff:.3f}")

print(f"\nAnswer: {mle_p3:.3f}") 