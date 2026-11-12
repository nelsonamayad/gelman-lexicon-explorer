# The USA Today Fallacy: averaging over states is not averaging over people.
size_corr <- 6 # how much the outcome rises with log population # <1>
set.seed(15) # <2>

pop <- c( # <3>
  California = 39.5, Texas = 29.1, Florida = 21.5,
  "New York" = 20.2, Pennsylvania = 13.0, Illinois = 12.8,
  Ohio = 11.8, Georgia = 10.7, "North Carolina" = 10.4,
  Michigan = 10.1, "New Jersey" = 9.3, Virginia = 8.6,
  Washington = 7.7, Arizona = 7.2, Massachusetts = 7.0,
  Tennessee = 6.9, Indiana = 6.8, Maryland = 6.2, Missouri = 6.2,
  Wisconsin = 5.9, Colorado = 5.8, Minnesota = 5.7,
  "South Carolina" = 5.1, Alabama = 5.0, Louisiana = 4.7,
  Kentucky = 4.5, Oregon = 4.2, Oklahoma = 4.0, Connecticut = 3.6,
  Utah = 3.3, Iowa = 3.2, Nevada = 3.1, Arkansas = 3.0,
  Mississippi = 3.0, Kansas = 2.9, "New Mexico" = 2.1,
  Nebraska = 2.0, Idaho = 1.8, "West Virginia" = 1.8, Hawaii = 1.5,
  "New Hampshire" = 1.4, Maine = 1.4, "Rhode Island" = 1.1,
  Montana = 1.1, Delaware = 1.0, "South Dakota" = 0.9,
  "North Dakota" = 0.8, Alaska = 0.7, Vermont = 0.6, Wyoming = 0.6
)
value <- 50 + size_corr * (log(pop) - mean(log(pop))) + rnorm(50, 0, 4) # <4>
cat("Average across the 50 states: ", round(mean(value), 1),
  "\nAverage across people: ", round(weighted.mean(value, pop), 1),
  "\n",
  sep = ""
)

plot(pop, value, # <5>
  log = "x", pch = 19, cex = sqrt(pop) / 2,
  col = adjustcolor("#2166ac", 0.6),
  xlab = "Population (millions)", ylab = "Outcome"
)
abline(h = mean(value), col = "#d6604d", lty = 2, lwd = 2)
abline(h = weighted.mean(value, pop), lwd = 2)

# Annotations
# 1. The page's control: how much the outcome rises with a state's population.
# 2. Fixes the random numbers so the run is reproducible.
# 3. Approximate 2020 populations of the 50 states, in millions.
# 4. A simulated outcome correlated with state size, as many urban-rural outcomes are.
# 5. The outcome against population, dots sized by population. The dashed line averages over states, the solid line over people, and they differ because the big states are different.
