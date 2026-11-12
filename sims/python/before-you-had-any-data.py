# What were you doing before you had any data? A prior predictive check.
import numpy as np
import matplotlib.pyplot as plt

s = 10  # prior sd on each logistic regression coefficient
K = 5   # number of standardized predictors
rng = np.random.default_rng(56)

# Linear predictor under the prior: intercept + sum of beta_k * x_k
beta = rng.normal(0, s, (4000, K))
x = rng.normal(size=(4000, K))
eta = rng.normal(size=4000) + (beta * x).sum(axis=1)
p = 1 / (1 + np.exp(-eta))  # implied predicted probabilities
extreme = np.mean((p < 0.01) | (p > 0.99))

print(f"Predicted probabilities below 1% or above 99%: {100 * extreme:.0f}%")
print("Try s = 1 for a prior that implies a reasonable spread.")

plt.hist(p, bins=np.arange(0, 1.001, 0.025), color="#2166ac")
plt.xlabel("Predicted probability implied by the prior")
plt.ylabel("Draws")
plt.show()
