# The capacity to be upset: flagging residuals that don't fit.
import numpy as np
import matplotlib.pyplot as plt

k = 2        # how hard to upset: flag residuals beyond k sd
shift = 1.2  # size of the real anomaly (sd units)
rng = np.random.default_rng(146)

t = np.arange(300)
real = (t >= 200) & (t < 240)  # the real anomaly
resid = rng.normal(np.where(real, shift, 0), 1)
flagged = np.abs(resid) > k

print(f"Flagged {(real & flagged).sum()} of the anomaly's 40 points, with "
      f"{(~real & flagged).sum()} false alarms elsewhere")

plt.axvspan(200, 240, color="#2166ac", alpha=0.1)
plt.scatter(t, resid, s=8, c=np.where(flagged, "#d6604d", "0.5"))
plt.axhline(k, color="black", linestyle="--")
plt.axhline(-k, color="black", linestyle="--")
plt.xlabel("Measurement")
plt.ylabel("Residual (sd units)")
plt.show()
