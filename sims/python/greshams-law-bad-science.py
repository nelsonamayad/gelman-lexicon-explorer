# Gresham's Law of bad science: bad papers crowd out good ones.
import numpy as np
import matplotlib.pyplot as plt

bad_share = 0.3  # share of incoming papers that are bad
bad_time = 4     # hours spent on each bad paper (vs 1 for a good one)
# Deterministic: no random numbers.

budget, incoming = 20, 20  # hours a week; papers a week


def good_read(share):
    n_good, n_bad = incoming * (1 - share), incoming * share
    frac_read = min(1, budget / (n_good + n_bad * bad_time))  # random order
    return n_good * frac_read


print(f"Good papers read per week: {good_read(bad_share):.1f} of "
      f"{incoming * (1 - bad_share):.0f} coming in")

shares = np.arange(0, 0.801, 0.05)
plt.plot(shares, [good_read(s) for s in shares], "o-", color="#2166ac")
plt.xlabel("Share of incoming papers that are bad")
plt.ylabel("Good papers read per week")
plt.show()
