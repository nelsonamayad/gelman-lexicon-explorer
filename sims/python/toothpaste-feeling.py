# That toothpaste feeling: jargon makes weak explanations feel better.
import numpy as np
import matplotlib.pyplot as plt

tingle = 1  # jargon boost to ratings
rng = np.random.default_rng(92)

jargon = np.arange(2000) % 2 == 0
quality = rng.normal(size=2000)
good = quality > 0
boost = np.where(jargon, tingle * np.where(good, 0.4, 1), 0)  # weak gain
rating = 4 + quality + boost + rng.normal(0, 0.5, 2000)
correct = rng.uniform(size=2000) < np.where(good, 0.85, 0.3)

groups = {}
for q, qname in [(good, "Good"), (~good, "Bad")]:
    for j, jname in [(~jargon, "plain"), (jargon, "jargon")]:
        g = q & j
        groups[f"{qname}, {jname}"] = rating[g]
        print(f"{qname} explanation, {jname}: rating "
              f"{rating[g].mean():.2f}, accuracy {correct[g].mean():.2f}")

plt.boxplot(list(groups.values()))
plt.xticks(range(1, 5), list(groups))
plt.ylabel("Rating of the explanation")
plt.show()
