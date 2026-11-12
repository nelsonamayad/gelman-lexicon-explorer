# Strongest-link Fallacy: a chain of evidence is as strong as all its links.
import numpy as np
import matplotlib.pyplot as plt

links = {"Randomization": 0.98,    # randomization was done properly
         "Measurement": 0.75,      # outcome measures what we care about
         "Power / noise": 0.6,     # estimate isn't noise
         "Generalization": 0.65}   # result generalizes to the policy
# Deterministic: no random numbers. If the links are independent, the
# whole chain holds with the product of their probabilities.

chain = {**links, "Whole chain": np.prod(list(links.values()))}
for k, v in chain.items():
    print(f"{k}: {v:.2f}")

plt.barh(list(chain)[::-1], list(chain.values())[::-1],
         color=["#d6604d"] + ["#2166ac"] * 4)
plt.xlim(0, 1)
plt.xlabel("Probability the link holds")
plt.tight_layout()
plt.show()
