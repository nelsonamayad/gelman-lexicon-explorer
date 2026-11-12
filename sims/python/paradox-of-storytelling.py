# The paradox of storytelling: the best stories are often the errors.
import numpy as np
import matplotlib.pyplot as plt

q = 0.01           # share of cases where the theory fails
err_rate = 0.005   # share of reports with gross errors
rng = np.random.default_rng(154)

N = 10000
real = rng.uniform(size=N) < q          # the theory fails for this case
truth = np.where(real, 3, 0)            # deviation, in sd units
gross = rng.uniform(size=N) < err_rate  # a detail that won't stand up
report = truth + rng.normal(size=N) + np.where(gross,
                                               rng.normal(0, 4, N), 0)

avg = rng.choice(report, 200)           # a random sample of cases
top = np.argsort(-np.abs(report))[:30]  # the 30 most striking stories
recheck = truth[top] + rng.normal(size=30)  # measure again, no gross error
print(f"Random sample: average deviation {avg.mean():.2f} "
      f"(se {avg.std(ddof=1) / np.sqrt(200):.2f})")
print(f"Of the 30 most striking stories, {real[top].sum()} are real "
      f"anomalies and {np.sum(np.abs(recheck) > 2)} hold up when rechecked")

rank = np.arange(1, 31)
plt.scatter(rank, np.abs(report[top]),
            c=np.where(real[top], "#2166ac", "#d6604d"))
plt.xlabel("Rank among the most striking stories (blue: real anomaly)")
plt.ylabel("Reported deviation (sd units)")
plt.show()
