# The year Jesus was born: center your predictors.
import numpy as np
import matplotlib.pyplot as plt

center = 0  # 0 (no centering), 1950, or "mean"
# Deterministic: no random numbers. Men's world records in the mile,
# 1913-1999, in seconds.
year = np.array([1913, 1915, 1923, 1931, 1933, 1934, 1937, 1942, 1942, 1942,
                 1943, 1944, 1945, 1954, 1954, 1957, 1958, 1962, 1964, 1965,
                 1966, 1967, 1975, 1975, 1979, 1980, 1981, 1981, 1981, 1985,
                 1993, 1999])
time = np.array([254.4, 252.6, 250.4, 249.2, 247.6, 246.8, 246.4, 246.2,
                 246.2, 244.6, 242.6, 241.6, 241.4, 239.4, 238.0, 237.2,
                 234.5, 234.4, 234.1, 233.6, 231.3, 231.1, 231.0, 229.4,
                 229.0, 228.8, 228.53, 228.40, 227.33, 226.32, 224.39,
                 223.13])
c0 = year.mean() if center == "mean" else center
X = np.column_stack([np.ones(len(year)), year - c0])
beta, *_ = np.linalg.lstsq(X, time, rcond=None)
s2 = np.sum((time - X @ beta) ** 2) / (len(year) - 2)
se = np.sqrt(s2 * np.diag(np.linalg.inv(X.T @ X)))
print(f"Intercept: {beta[0]:.1f} (se {se[0]:.2f}), the record time in "
      f"the year {c0:.0f}")
print(f"Slope: {beta[1]:.3f} seconds per year (se {se[1]:.3f})")

plt.scatter(year, time, color="black")
plt.plot(year, beta[0] + beta[1] * (year - c0), color="#2166ac",
         linewidth=2)
plt.xlabel("Year")
plt.ylabel("World record, mile (seconds)")
plt.show()
