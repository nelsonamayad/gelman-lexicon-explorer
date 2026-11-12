# Eureka bias: refusing to let go of a discovery.
phi <- 0.05 # weight the eureka-biased researcher gives new data # <1>
set.seed(72) # <2>

se <- 0.3
first <- max(rnorm(20, 0, se)) # the "discovery": best of 20 noisy looks # <3>
y <- rnorm(20, 0, se) # 20 follow-ups; the true effect is zero
w0 <- 1 / se^2
w <- 1 / se^2
k <- 1:20
neutral <- (first * w0 + cumsum(y) * w) / (w0 + k * w) # <4>
eureka <- (first * w0 + cumsum(y) * w * phi) / (w0 + k * w * phi) # <5>

cat("Discovery: ", round(first, 2), " | belief after 20 follow-ups: ",
  "neutral ", round(tail(neutral, 1), 2), ", eureka-biased ",
  round(tail(eureka, 1), 2), "\n",
  sep = ""
)

matplot(0:20, cbind(c(first, neutral), c(first, eureka)), # <6>
  type = "l",
  lty = 1, lwd = 2, col = c("#2166ac", "#d6604d"),
  xlab = "Follow-up studies", ylab = "Belief about the effect"
)
abline(h = 0, lty = 2)
legend("topright", c("Neutral updater", "Eureka-biased"),
  col = c("#2166ac", "#d6604d"), lwd = 2, bty = "n"
)

# Annotations
# 1. The page's control: how much weight the eureka-biased researcher gives each new study, relative to the discovery.
# 2. Fixes the random numbers so the run is reproducible.
# 3. The discovery: the best of 20 noisy looks at an effect that is really zero.
# 4. A neutral updater weights the discovery and each follow-up equally, so belief sinks toward zero.
# 5. The eureka-biased updater discounts every follow-up, so the discovery keeps its grip.
# 6. Belief after each follow-up study under the two rules.
