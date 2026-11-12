# Passive Corruption: silence lets bad work take over a field.
import matplotlib.pyplot as plt

adv = 0.12    # growth advantage of bad work
speak = 0.05  # probability someone who knows speaks up, per year
# Deterministic: no random numbers. Bad work starts at 10% of the field.


def run(s):
    bad = [0.1]
    for _ in range(40):
        b = bad[-1] * (1 + adv) * (1 - s)
        bad.append(b / (b + 1 - bad[-1]))
    return bad


share = {"Your setting": run(speak), "Total silence": run(0),
         "Active correction": run(0.3)}
for (k, v), c in zip(share.items(), ["#2166ac", "#d6604d", "#1a9850"]):
    print(f"{k}: {100 * v[-1]:.0f}% bad work after 40 years")
    plt.plot(v, color=c, linewidth=2, label=k)
plt.ylim(0, 1)
plt.xlabel("Year")
plt.ylabel("Share of the field that is bad work")
plt.legend()
plt.show()
