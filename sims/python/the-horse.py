# The Horse: keep beating it, or the refuted finding keeps spreading.
import numpy as np
import matplotlib.pyplot as plt

q_beat = 0.5   # share of new citers who learn of the refutation
q_stop = 0.1   # the same share if critics stop
growth = 1.15  # citation growth factor
# Deterministic: no random numbers.

years = np.arange(26)
keep = 100 * (growth * (1 - q_beat)) ** years  # uncritical citations/year
stop = 100 * (growth * (1 - q_stop)) ** years
print(f"After 25 years, uncritical citations per year: {keep[-1]:.1f} if "
      f"critics keep at it, {stop[-1]:.1f} if they stop")

plt.semilogy(years, keep, color="#2166ac", linewidth=2,
             label="Critics keep beating the horse")
plt.semilogy(years, stop, color="#d6604d", linewidth=2,
             label="Critics stop: 'everyone knows'")
plt.xlabel("Year")
plt.ylabel("Uncritical citations per year")
plt.legend()
plt.show()
