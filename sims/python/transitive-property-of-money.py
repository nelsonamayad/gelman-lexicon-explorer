# The transitive property of money: wealth buys a hearing on any topic.
import numpy as np
import matplotlib.pyplot as plt

w = 1  # weight the audience gives to wealth
rng = np.random.default_rng(155)

investor = np.repeat([False, True], 100)
expertise = np.where(investor, rng.normal(-1, 1, 200),
                     rng.normal(1, 1, 200))
wealth = np.where(investor, rng.normal(2, 0.7, 200), rng.normal(0, 0.7, 200))
cred = expertise + w * wealth + rng.normal(0, 0.5, 200)
heard = np.argsort(-cred).argsort() < 20       # the 20 most-heard voices
best = np.argsort(-expertise).argsort() < 20   # the 20 who know most
print(f"{np.sum(heard & investor)} of the 20 most-heard voices are tech "
      "investors")
print(f"Average expertise: most heard {expertise[heard].mean():.2f}, "
      f"most expert {expertise[best].mean():.2f}")

for g, c, name in [(~investor, "#2166ac", "Domain expert"),
                   (investor, "#d6604d", "Tech investor")]:
    plt.scatter(expertise[g & ~heard], cred[g & ~heard], facecolors="none",
                edgecolors=c)
    plt.scatter(expertise[g & heard], cred[g & heard], color=c,
                label=f"{name} (filled: most heard)")
plt.xlabel("Expertise on the topic")
plt.ylabel("Credibility with audience")
plt.legend()
plt.show()
