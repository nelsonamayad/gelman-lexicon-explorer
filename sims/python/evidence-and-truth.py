# Evidence and Truth: they're different.
import numpy as np
import matplotlib.pyplot as plt

pi_true = 0.3  # share of claims that are true
signal = 1.5   # typical evidence strength (z) for true claims
rng = np.random.default_rng(85)

true_claim = rng.uniform(size=3000) < pi_true
z = rng.normal(np.where(true_claim, signal, 0), 1)  # each claim's evidence
strong = z > 1.96

print(f"Claims with strong evidence that are false: "
      f"{100 * np.mean(~true_claim[strong]):.0f}%")
print(f"True claims with only weak evidence: "
      f"{100 * np.mean(~strong[true_claim]):.0f}%")

bins = np.arange(np.floor(z.min()), np.ceil(z.max()) + 0.25, 0.25)
plt.hist(z[~true_claim], bins, color="#d6604d", alpha=0.5,
         label="False claims")
plt.hist(z[true_claim], bins, color="#2166ac", alpha=0.5,
         label="True claims")
plt.axvline(1.96, color="black", linestyle="--")
plt.xlabel("Strength of evidence (z)")
plt.ylabel("Claims")
plt.legend()
plt.show()
