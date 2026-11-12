# Just because something is counterintuitive doesn't mean it's true.
power <- 0.5 # power of each study # <1>
set.seed(76) # <2>

shift <- qnorm(0.975) + qnorm(power) # effect in standard-error units # <3>
priors <- c(0.02, 0.05, 0.1, 0.2, 0.3, 0.5, 0.7, 0.9)
ppv <- sapply(priors, function(p) { # share of significant results that # <4>
  real <- runif(20000) < p # are real, for prior probability p
  z <- rnorm(20000, ifelse(real, shift, 0), 1)
  sig <- abs(z) > 1.96
  mean(real[sig])
})
theory <- priors * power / (priors * power + (1 - priors) * 0.05) # <5>
print(round(cbind(prior = priors, simulated = ppv, theory = theory), 2))

plot(priors, ppv, # <6>
  log = "x", pch = 19, col = "#2166ac", ylim = c(0, 1),
  xlab = "Prior probability the hypothesis is true (log scale)",
  ylab = "Share of significant results that are true"
)
lines(priors, theory, col = "#d6604d")

# Annotations
# 1. The page's control: the power of each study.
# 2. Fixes the random numbers so the run is reproducible.
# 3. The z-score shift that gives a true hypothesis the chosen power.
# 4. For each prior probability, simulate 20,000 hypotheses, test them and ask what share of the significant results are true.
# 5. The same quantity from Bayes' rule.
# 6. Counterintuitive hypotheses are the ones with low prior probability, at the left: a significant result for one is usually false.
