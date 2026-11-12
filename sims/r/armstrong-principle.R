# The (Lance) Armstrong Principle: promise more than you can deliver.
promise <- 0.5 # promised effect T # <1>
kappa <- 3 # pressure to deliver
set.seed(64) # <2>

honest <- rnorm(2000, 0.2, 0.25) # <3>
p_cheat <- ifelse(honest < promise, 1 - exp(-kappa * (promise - honest)), 0) # <4>
cheat <- runif(2000) < p_cheat
reported <- ifelse(cheat, promise + abs(rnorm(2000, 0, 0.05)), honest) # <5>

cat("Share who cheat: ", round(100 * mean(cheat)), "%\n", sep = "")
cat(
  "Average reported effect:", round(mean(reported), 2),
  "(honest average 0.20)\n"
)

breaks <- seq(min(reported) - 0.05, max(reported) + 0.05, length.out = 60)
hist(reported, # <6>
  breaks = breaks, col = "#2166ac", border = "white",
  main = "", xlab = "Reported effect", ylab = "Researchers"
)
hist(reported[cheat],
  breaks = breaks, col = "#d6604d", border = "white",
  add = TRUE
)
abline(v = promise, lty = 2)

# Annotations
# 1. The page's controls: the promised effect and the pressure to deliver it.
# 2. Fixes the random numbers so the run is reproducible.
# 3. What each researcher would honestly find.
# 4. The further an honest result falls short of the promise, the more likely the researcher is to cheat. The pressure parameter sets how quickly.
# 5. Cheaters report the promise, or a little more. Everyone else reports what they found.
# 6. The histogram of reported effects. The red spike at the promise is the cheating.
