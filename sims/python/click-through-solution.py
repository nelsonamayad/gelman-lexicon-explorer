# The Click-Through Solution: three layers for three audiences.
import numpy as np
import matplotlib.pyplot as plt

layer = 2  # 1: grab attention, 2: compare, 3: check the numbers
rng = np.random.default_rng(125)

names = ["Avalon", "Brookfield", "Cedar Falls", "Dunmore", "Eastport",
         "Fairview", "Glenwood", "Harbor City", "Ironton", "Juniper",
         "Kingsley", "Lakeside"]
y2015 = rng.uniform(20, 80, 12)
region = rng.choice(["North", "South", "Coast"], 12)
y2025 = y2015 + rng.normal(5, 8, 12)
cols = {"North": "#2166ac", "South": "#d6604d", "Coast": "#1a9850"}
colors = [cols[r] for r in region]

if layer == 1:    # bubbles: eye-catching, hard to compare
    plt.scatter(rng.uniform(size=12), rng.uniform(size=12), s=y2025 * 20,
                c=colors, alpha=0.6)
    plt.axis("off")
    plt.show()
elif layer == 2:  # positions on a common scale: easy to compare
    o = np.argsort(y2025)
    y = np.arange(12)
    plt.scatter(y2015[o], y, facecolors="none", edgecolors="black",
                label="2015")
    plt.scatter(y2025[o], y, c=[colors[i] for i in o], label="2025")
    plt.yticks(y, [names[i] for i in o])
    plt.xlabel("Value")
    plt.legend()
    plt.tight_layout()
    plt.show()
else:             # the numbers, for checking and reuse
    for i in range(12):
        print(f"{names[i]:12s} {region[i]:6s} {y2015[i]:6.1f} {y2025[i]:6.1f}"
              f" {y2025[i] - y2015[i]:+6.1f}")
