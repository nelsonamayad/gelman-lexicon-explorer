# Physics is like Brazil, statistics is like Chile: how soon do you reach
# the frontier?
import numpy as np
import matplotlib.pyplot as plt

trek = 8      # Brazil: years of study before reaching the frontier
p_hit = 0.25  # Chile: chance a routine project hits an open problem
rng = np.random.default_rng(143)


def reach(first_year, p):  # year each of 1000 students first gets there
    years = np.arange(1, 16)
    hit = (years >= first_year) & (rng.uniform(size=(1000, 15)) < p)
    return np.where(hit.any(axis=1), years[hit.argmax(axis=1)], np.inf)


physics, statistics = reach(trek, 0.35), reach(1, p_hit)
y = np.arange(16)
share_p = [(physics <= k).mean() for k in y]
share_s = [(statistics <= k).mean() for k in y]
print(f"Reached the frontier by year 5: physics {100 * share_p[5]:.0f}%, "
      f"statistics {100 * share_s[5]:.0f}%")

plt.step(y, share_p, where="post", color="#d6604d", linewidth=2,
         label="Physics (Brazil)")
plt.step(y, share_s, where="post", color="#2166ac", linewidth=2,
         label="Statistics (Chile)")
plt.ylim(0, 1)
plt.xlabel("Years of study")
plt.ylabel("Share who have worked on an open problem")
plt.legend()
plt.show()
