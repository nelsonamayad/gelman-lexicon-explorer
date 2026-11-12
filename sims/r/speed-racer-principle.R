# The Speed Racer Principle: an interaction on one scale vanishes on another.
growth <- 0.15 # common growth rate per period # <1>
ratio <- 2.5 # group A starts this many times higher
set.seed(54) # <2>

t <- sample(0:6, 400, replace = TRUE)
a <- rbinom(400, 1, 0.5)
y <- 10 * ifelse(a == 1, ratio, 1) * exp(growth * t + rnorm(400, 0, 0.1)) # <3>
raw <- summary(lm(y ~ t * a))$coefficients["t:a", 1:2] # <4>
logs <- summary(lm(log(y) ~ t * a))$coefficients["t:a", 1:2] # <5>
cat("Interaction (time x group), estimate and se:\n",
  "raw scale ", round(raw[1], 2), " (", round(raw[2], 2), "), ",
  "log scale ", round(logs[1], 3), " (", round(logs[2], 3), ")\n",
  sep = ""
)

par(mfrow = c(1, 2)) # <6>
plot(jitter(t), y,
  pch = 19, cex = 0.5, main = "Raw scale",
  col = ifelse(a == 1, "#d6604d", "#2166ac"), xlab = "Time", ylab = "y"
)
plot(jitter(t), log(y),
  pch = 19, cex = 0.5, main = "Log scale",
  col = ifelse(a == 1, "#d6604d", "#2166ac"), xlab = "Time",
  ylab = "log y"
)

# Annotations
# 1. The page's controls: the common growth rate and how much higher group A starts.
# 2. Fixes the random numbers so the run is reproducible.
# 3. Both groups grow at the same percentage rate; one starts higher.
# 4. On the raw scale the time-by-group interaction is large and significant: the headline finding.
# 5. On the log scale it vanishes. The finding came from the unexamined assumption about scale.
# 6. The same data on both scales.
