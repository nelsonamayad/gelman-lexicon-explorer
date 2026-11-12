# Multiple Comparisons: classical tests vs a multilevel model.
import numpy as np
import matplotlib.pyplot as plt

tau = 0.1    # spread of true effects
sigma = 0.5  # standard error of each estimate
rng = np.random.default_rng(25)

theta = rng.normal(0, tau, 50)   # 50 true effects, mostly tiny
y = rng.normal(theta, sigma)     # their noisy estimates

# Multilevel model (empirical Bayes): shrink toward the mean
mu = y.mean()
tau2 = max(0, np.mean((y - mu) ** 2) - sigma ** 2)
B = tau2 / (tau2 + sigma ** 2)
pm = mu + B * (y - mu)           # posterior means
psd = np.sqrt(B) * sigma + 1e-9  # posterior sds

claim_classic = np.abs(y) > 1.96 * sigma
claim_ml = (B > 0) & (np.abs(pm) > 1.96 * psd)
wrong_classic = claim_classic & (np.sign(y) != np.sign(theta))
wrong_ml = claim_ml & (np.sign(pm) != np.sign(theta))
print(f"Classical: {claim_classic.sum()} 'significant' effects, "
      f"{wrong_classic.sum()} with the wrong sign")
print(f"Multilevel: {claim_ml.sum()} confident claims, "
      f"{wrong_ml.sum()} with the wrong sign")

plt.scatter(theta, y, color="#d6604d", label="Raw estimate")
plt.scatter(theta[claim_classic], y[claim_classic], s=120,
            facecolors="none", edgecolors="black", label="'Significant'")
plt.scatter(theta, pm, color="#2166ac", label="Multilevel estimate")
plt.axhline(1.96 * sigma, color="black", linestyle="--")
plt.axhline(-1.96 * sigma, color="black", linestyle="--")
plt.xlabel("True effect")
plt.ylabel("Estimate")
plt.legend()
plt.show()
