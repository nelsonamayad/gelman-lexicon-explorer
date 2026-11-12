# The John Yoo Line: once trust is lost, careful work goes unnoticed.
import numpy as np
import matplotlib.pyplot as plt

lapse_start = 15   # when the author gets careless (piece #)
lapse_length = 12  # how long the lapse lasts
line = 0.5         # trust threshold (the line)
rng = np.random.default_rng(47)

# Belief that the author is reliable (right 90% of the time) rather than a
# hack (30%). Below the line, readers mostly stop paying attention.
log_odds = 3
trust = []
for t in range(1, 61):
    careless = lapse_start < t <= lapse_start + lapse_length
    good = rng.uniform() < (0.3 if careless else 0.9)
    noticed = 1 / (1 + np.exp(-log_odds)) >= line or rng.uniform() < 0.15
    if noticed:
        log_odds += np.log(0.9 / 0.3) if good else np.log(0.1 / 0.7)
    log_odds = min(12, max(-12, log_odds))
    trust.append(1 / (1 + np.exp(-log_odds)))
trust = np.array(trust)
pieces = np.arange(1, 61)
below = pieces[trust < line]
if below.size:
    print(f"Trust falls below the line at piece {below[0]}")
    back = pieces[(trust >= line) & (pieces > below[0])]
    print(f"Back above the line at piece {back[0]}" if back.size
          else "Trust never recovers within 60 pieces")
else:
    print("Trust never falls below the line")

plt.axvspan(lapse_start + 0.5, lapse_start + lapse_length + 0.5,
            color="#d6604d", alpha=0.1)
plt.plot(pieces, trust, color="#2166ac", linewidth=2)
plt.axhline(line, color="black", linestyle="--")
plt.ylim(0, 1)
plt.xlabel("Piece")
plt.ylabel("Audience trust")
plt.show()
