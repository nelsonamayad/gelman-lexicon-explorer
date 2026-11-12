# The Secret Weapon: fit the same model to each year, then plot them all.
n_per_year <- 300 # respondents per survey # <1>
trend <- "Rising" # or "Flat", "Rise and fall"
set.seed(11) # <2>

years <- seq(1972, 2024, by = 2)
truth <- function(yr) { # <3>
  t <- (yr - 1972) / 52
  switch(trend,
    Rising = 0.1 + 0.5 * t,
    Flat = 0.3 + 0 * t,
    "Rise and fall" = 0.1 + 1.2 * t * (1 - t) * 1.6
  )
}
fits <- t(sapply(years, function(year) { # <4>
  x <- rnorm(n_per_year)
  y <- 1 + truth(year) * x + rnorm(n_per_year)
  summary(lm(y ~ x))$coefficients["x", 1:2] # estimate and se
}))
inside <- abs(fits[, 1] - truth(years)) <= fits[, 2] # <5>
cat(
  sum(inside), "of", length(years), "intervals (+/- 1 se) cover the",
  "true coefficient\n"
)

plot(years, fits[, 1], # <6>
  pch = 19,
  ylim = range(fits[, 1] - fits[, 2], fits[, 1] + fits[, 2]),
  xlab = "Year", ylab = "Coefficient estimate"
)
segments(years, fits[, 1] - fits[, 2], years, fits[, 1] + fits[, 2])
lines(years, truth(years), col = "#d6604d", lwd = 2, lty = 2)

# Annotations
# 1. The page's controls: respondents per survey and the true pattern over time.
# 2. Fixes the random numbers so the run is reproducible.
# 3. The true coefficient in each year.
# 4. The secret weapon: fit the same regression separately to each year's survey and keep the coefficient and its standard error.
# 5. How many of the one-standard-error intervals cover the truth (about two thirds is expected).
# 6. All the estimates plotted together against the true trend. No single year shows the pattern; the set of years does.
