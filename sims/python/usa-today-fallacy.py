# The USA Today Fallacy: averaging over states is not averaging over people.
import numpy as np
import matplotlib.pyplot as plt

size_corr = 6  # how much the outcome rises with log population
rng = np.random.default_rng(15)

pop = {"California": 39.5, "Texas": 29.1, "Florida": 21.5,
       "New York": 20.2, "Pennsylvania": 13.0, "Illinois": 12.8,
       "Ohio": 11.8, "Georgia": 10.7, "North Carolina": 10.4,
       "Michigan": 10.1, "New Jersey": 9.3, "Virginia": 8.6,
       "Washington": 7.7, "Arizona": 7.2, "Massachusetts": 7.0,
       "Tennessee": 6.9, "Indiana": 6.8, "Maryland": 6.2, "Missouri": 6.2,
       "Wisconsin": 5.9, "Colorado": 5.8, "Minnesota": 5.7,
       "South Carolina": 5.1, "Alabama": 5.0, "Louisiana": 4.7,
       "Kentucky": 4.5, "Oregon": 4.2, "Oklahoma": 4.0, "Connecticut": 3.6,
       "Utah": 3.3, "Iowa": 3.2, "Nevada": 3.1, "Arkansas": 3.0,
       "Mississippi": 3.0, "Kansas": 2.9, "New Mexico": 2.1,
       "Nebraska": 2.0, "Idaho": 1.8, "West Virginia": 1.8, "Hawaii": 1.5,
       "New Hampshire": 1.4, "Maine": 1.4, "Rhode Island": 1.1,
       "Montana": 1.1, "Delaware": 1.0, "South Dakota": 0.9,
       "North Dakota": 0.8, "Alaska": 0.7, "Vermont": 0.6, "Wyoming": 0.6}
p = np.array(list(pop.values()))
value = (50 + size_corr * (np.log(p) - np.log(p).mean())
         + rng.normal(0, 4, 50))
print(f"Average across the 50 states: {value.mean():.1f}")
print(f"Average across people: {np.average(value, weights=p):.1f}")

plt.scatter(p, value, s=10 * p, color="#2166ac", alpha=0.6)
plt.xscale("log")
plt.axhline(value.mean(), color="#d6604d", linestyle="--", linewidth=2,
            label="Average of states")
plt.axhline(np.average(value, weights=p), color="black", linewidth=2,
            label="Average of people")
plt.xlabel("Population (millions)")
plt.ylabel("Outcome")
plt.legend()
plt.show()
