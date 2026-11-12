# End of novel. Beginning of job: when to stop thinking and start finishing.
tau <- 6 # time scale of insight (weeks) # <1>
cost <- 2 # cost of delay per week
# Deterministic: no random numbers.

t <- seq(0, 40, by = 0.25)
value <- 100 * (1 - exp(-t / tau)) # value of the analysis after t weeks # <2>
net <- value - cost * t # <3>
t_star <- max(0, tau * log(100 / (cost * tau))) # where gains = cost # <4>

cat("Stop thinking and start finishing after about ", round(t_star, 1),
  " weeks,\nwhen the analysis has reached ",
  round(100 * (1 - exp(-t_star / tau))), "% of its potential value\n",
  sep = ""
)

plot(t, value, # <5>
  type = "l", lwd = 2, col = "#2166ac", ylim = range(net, 100),
  xlab = "Weeks of thinking", ylab = "Value"
)
lines(t, net, lwd = 2, col = "#d6604d")
abline(v = t_star, lty = 2)
legend("bottomright", c("Value of the analysis", "Value minus cost of delay"),
  col = c("#2166ac", "#d6604d"), lwd = 2, bty = "n"
)

# Annotations
# 1. The page's controls: how quickly insight accumulates and what each week of delay costs. There is no seed: the model is deterministic.
# 2. The value of the analysis after t weeks of thinking, with diminishing returns.
# 3. The value net of the cost of delay.
# 4. The moment to stop thinking and start finishing: when another week's insight no longer pays for the delay.
# 5. Both curves, with the stopping time dashed. The novel ends; the job begins.
