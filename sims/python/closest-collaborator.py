# Your closest collaborator: you, six months ago.
import numpy as np
import matplotlib.pyplot as plt

doc_frac = 0.3  # fraction of decisions documented
tau = 4         # memory half-life (months)
rng = np.random.default_rng(104)

D, lam = 40, np.log(2) / tau
months = np.arange(25)
expected = D * (doc_frac + (1 - doc_frac) * np.exp(-lam * months))
documented = np.arange(D) < doc_frac * D
recovered = [np.sum(documented | (rng.uniform(size=D) < np.exp(-lam * t)))
             for t in months]

print(f"Decisions you can reconstruct after 6 months: about "
      f"{expected[6]:.0f} of 40")
print(f"After two years: about {expected[24]:.0f} of 40")

plt.plot(months, recovered, "o", color="#2166ac")
plt.plot(months, expected, color="#2166ac")
plt.axhline(doc_frac * D, color="#d6604d", linestyle="--")
plt.ylim(0, D)
plt.xlabel("Months later")
plt.ylabel("Decisions you can reconstruct")
plt.show()
