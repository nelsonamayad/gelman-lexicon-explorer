# Research Incumbency Rule: once published, a flaw has to be much worse to
# be corrected.
import numpy as np
import matplotlib.pyplot as plt

t_pre = 1.5     # severity that blocks publication in review
t_post = 3      # severity needed to correct after publication
p_notice = 0.5  # chance a reviewer notices a flaw
rng = np.random.default_rng(89)

s = rng.exponential(1 / 0.8, 5000)  # severity of each paper's worst flaw
blocked = (rng.uniform(size=5000) < p_notice) & (s > t_pre)
corrected = ~blocked & (s > t_post)
counts = {"Rejected in review": blocked.sum(),
          "Corrected after publication": corrected.sum(),
          "Published; serious flaw persists":
              np.sum(~blocked & ~corrected & (s > t_pre)),
          "Published; minor or no flaw": np.sum(s <= t_pre)}
for k, v in counts.items():
    print(f"{k}: {v}")

plt.barh(list(counts), list(counts.values()), color="#2166ac")
plt.xlabel("Papers (of 5000)")
plt.tight_layout()
plt.show()
