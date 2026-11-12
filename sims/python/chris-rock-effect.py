# The Chris Rock Effect: births by day of year, averaged over weekdays.
import numpy as np
import matplotlib.pyplot as plt

rng = np.random.default_rng(42)

# Day of year: effect on log births (Halloween is a smaller dip)
holidays = {1: -0.3, 185: -0.3, 245: -0.3, 304: -0.05, 327: -0.3, 359: -0.3}
doy = np.arange(1, 366)
hol = np.array([holidays.get(d, 0) for d in doy])
near = np.array([-0.06 if d not in holidays
                 and (d - 1 in holidays or d + 1 in holidays) else 0
                 for d in doy])
series, weekday_sum, weekday_n = [], np.zeros(365), np.zeros(365)
for k in range(5):  # five years; the weekday shifts each year
    dow = (doy - 1 + k) % 7
    weekend = dow >= 5
    births = 10000 * np.exp(np.where(weekend, -0.22, 0)
                            + 0.05 * np.sin(2 * np.pi * (doy - 101) / 365)
                            + hol + near + rng.normal(0, 0.025, 365))
    series.append(births)
    weekday_sum += np.where(weekend, 0, births)
    weekday_n += ~weekend
avg = weekday_sum / weekday_n

fig, (top, bottom) = plt.subplots(2, 1, figsize=(8, 6))
top.plot(np.concatenate(series), color="0.5", linewidth=0.5)
top.set_title("Raw daily series")
bottom.plot(doy, avg, color="#2166ac")
for d in holidays:
    bottom.axvline(d, color="#d6604d", linestyle=":")
bottom.set_title("Day of year, averaged over weekdays")
bottom.set_xlabel("Day of year")
plt.tight_layout()
plt.show()
print("Lowest weekday averages fall on days:", np.argsort(avg)[:6] + 1)
