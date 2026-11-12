# The Error-Reversal Heuristic: checking harder when errors hurt the story.
import numpy as np
import matplotlib.pyplot as plt

p_conv = 0.2    # chance of catching an error that helps the story
p_inconv = 0.8  # chance of catching an error that hurts the story
rng = np.random.default_rng(144)

est = rng.normal(0, 0.2, 3000)  # the true effect is zero
has_err = rng.uniform(size=3000) < 0.3
err = np.where(has_err, rng.normal(0, 0.6, 3000), 0)
caught = has_err & (rng.uniform(size=3000) < np.where(err > 0, p_conv,
                                                       p_inconv))
published = est + np.where(caught, 0, err)

print(f"Average published estimate: {published.mean():.3f} "
      "(true effect: 0)")

bins = np.linspace(min(est.min(), published.min()) - 0.1,
                   max(est.max(), published.max()) + 0.1, 60)
plt.hist(est, bins, color="#2166ac", alpha=0.5, label="Honest estimates")
plt.hist(published, bins, color="#d6604d", alpha=0.5, label="Published")
plt.axvline(0, color="black", linewidth=2)
plt.xlabel("Estimate")
plt.ylabel("Studies")
plt.legend()
plt.show()
