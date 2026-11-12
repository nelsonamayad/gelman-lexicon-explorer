# Deference Trap: errors spread through a literature that never checks itself.
import numpy as np
import matplotlib.pyplot as plt

base_error = 0.1  # chance a new study is wrong on its own
inherit = 0.4     # chance a wrong foundation compromises a study
check_rate = 0.2  # share of wrong studies caught by meta-science each round
rng = np.random.default_rng(87)


def run(check):
    wrong = rng.uniform(size=100) < base_error
    flagged = np.zeros(100, dtype=bool)
    share = [wrong.mean()]
    for _ in range(15):      # 15 generations of 100 studies
        flagged |= wrong & (rng.uniform(size=wrong.size) < check)
        usable = np.flatnonzero(~flagged)
        if usable.size == 0:
            usable = np.arange(wrong.size)
        new = rng.uniform(size=100) < base_error
        for _ in range(3):   # each new study builds on three earlier ones
            cited = rng.choice(usable, 100)
            new |= wrong[cited] & (rng.uniform(size=100) < inherit)
        wrong = np.concatenate([wrong[-200:], new])  # keep the last 200
        flagged = np.concatenate([flagged[-200:], np.zeros(100, bool)])
        share.append(new.mean())
    return share


deference, checked = run(0), run(check_rate)
print(f"Compromised after 15 generations: {100 * deference[-1]:.0f}% with "
      f"pure deference, {100 * checked[-1]:.0f}% with meta-science checking")

plt.plot(deference, color="#d6604d", linewidth=2, label="No meta-science")
plt.plot(checked, color="#2166ac", linewidth=2,
         label="With meta-science checking")
plt.ylim(0, 1)
plt.xlabel("Generation")
plt.ylabel("Share of new studies compromised")
plt.legend()
plt.show()
