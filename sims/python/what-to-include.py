# What to include: print only the digits that survive replication.
import math
import numpy as np

se = 0.3  # standard error of the estimate
rng = np.random.default_rng(108)

est = 3.141593 + rng.normal(0, se, 15)  # 15 replications of the estimate
for i, e in enumerate(est, 1):
    print(f"{i:2d} {e:10.6f}")
dec = max(0, -math.floor(math.log10(se)))  # decimals worth reporting
print(f"A sensible report: {est[0]:.{dec}f} ({se:.{dec}f})")
