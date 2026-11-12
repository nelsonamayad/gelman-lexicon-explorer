# The "What does not kill my statistical significance makes it stronger"
# fallacy: significance found through noise is weaker evidence.
import numpy as np
import matplotlib.pyplot as plt

theta = 0.2  # true effect
rng = np.random.default_rng(62)

ses = [0.05, 0.1, 0.15, 0.2, 0.3, 0.4, 0.5, 0.75, 1]
exaggeration = []
for se in ses:
    e = rng.normal(theta, se, 20000)
    sig = e[np.abs(e) > 1.96 * se]      # the significant estimates
    exaggeration.append(np.abs(sig).mean() / theta)
    print(f"se {se:.2f}: power {sig.size / 20000:.2f}, exaggeration "
          f"{exaggeration[-1]:.1f}x, wrong sign {np.mean(sig < 0):.3f}")

plt.plot(ses, exaggeration, "o-", color="#d6604d")
plt.axhline(1, color="black", linestyle="--")
plt.xlabel("Standard error (noise)")
plt.ylabel("Exaggeration of significant estimates")
plt.show()
