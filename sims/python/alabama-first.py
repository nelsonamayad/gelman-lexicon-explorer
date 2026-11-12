# Alabama First: the same 50 states sorted three ways.
import numpy as np
import matplotlib.pyplot as plt

order_by = "alphabetical"  # "alphabetical", "value" or "region"
region_gap = 6             # size of regional differences
rng = np.random.default_rng(14)

regions = {
    "Northeast": "Connecticut Maine Massachusetts New_Hampshire New_Jersey "
                 "New_York Pennsylvania Rhode_Island Vermont",
    "Midwest": "Illinois Indiana Iowa Kansas Michigan Minnesota Missouri "
               "Nebraska North_Dakota Ohio South_Dakota Wisconsin",
    "South": "Alabama Arkansas Delaware Florida Georgia Kentucky Louisiana "
             "Maryland Mississippi North_Carolina Oklahoma South_Carolina "
             "Tennessee Texas Virginia West_Virginia",
    "West": "Alaska Arizona California Colorado Hawaii Idaho Montana Nevada "
            "New_Mexico Oregon Utah Washington Wyoming",
}
effect = {"Northeast": 1, "Midwest": 0, "South": -1, "West": 0.4}
states = sorted((s.replace("_", " "), r) for r, names in regions.items()
                for s in names.split())
rows = [(s, r, 50 + region_gap * effect[r] + rng.normal(0, 3))
        for s, r in states]

if order_by == "value":
    rows.sort(key=lambda d: -d[2])
elif order_by == "region":
    rows.sort(key=lambda d: (d[1], -d[2]))
colors = {"Midwest": "#2166ac", "Northeast": "#d6604d", "South": "#4daf4a",
          "West": "#984ea3"}
y = np.arange(len(rows))[::-1]
plt.figure(figsize=(6, 10))
plt.scatter([d[2] for d in rows], y, c=[colors[d[1]] for d in rows])
plt.yticks(y, [d[0] for d in rows], fontsize=7)
plt.xlabel("Simulated outcome")
plt.tight_layout()
plt.show()
print(f"Regional gap (Northeast minus South): {2 * region_gap} points")
