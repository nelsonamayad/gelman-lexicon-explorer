# Statistical Chemotherapy: inflate the standard errors until the
# inconvenient result goes away.
from statistics import NormalDist
import numpy as np
import matplotlib.pyplot as plt

z_key = 3        # z of the key result (before chemo)
z_placebo = 2.3  # z of the placebo test (before chemo)
dose = 1.3       # chemo dose: standard-error multiplier
# Deterministic: no random numbers.

cdf = np.vectorize(NormalDist().cdf)


def p_value(z, c):
    return 2 * (1 - cdf(abs(z) / c))


pk, pp = p_value(z_key, dose), p_value(z_placebo, dose)
print(f"At dose {dose}: key result p = {pk:.3f}, placebo test p = {pp:.3f}")
if pk < 0.05 and pp >= 0.05:
    print('Treatment "successful": the placebo test has gone away and the '
          "key result survives.")
elif pk < 0.05:
    print("Both still significant: needs a stronger dose.")
else:
    print("Too strong: the key result is gone too.")

c = np.arange(1, 2.51, 0.05)
plt.semilogy(c, p_value(z_key, c), color="#2166ac", linewidth=2,
             label="Key result")
plt.semilogy(c, p_value(z_placebo, c), color="#d6604d", linewidth=2,
             label="Placebo test (should be null)")
plt.axhline(0.05, color="black", linestyle="--")
plt.axvline(dose, color="0.6")
plt.xlabel("Standard-error multiplier")
plt.ylabel("p-value")
plt.legend()
plt.show()
