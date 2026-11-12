# More Vampirical Than Empirical: theories that explain away every failure.
m <- 0.85 # probability a failure is explained away # <1>
lr <- 0.4 # likelihood ratio of each failed test
set.seed(47) # <2>

# Belief in a false theory, starting at 80%, over 20 tests
emp <- vam <- log(4)
belief <- matrix(0.8, 21, 2, dimnames = list(NULL, c(
  "Empirical",
  "Vampirical"
)))
for (k in 1:20) {
  success <- runif(1) < 0.08 # occasional false positive # <3>
  l <- if (success) log(1 / lr) else log(lr)
  emp <- emp + l # <4>
  vam <- vam + if (success || runif(1) >= m) l else 0 # <5>
  belief[k + 1, ] <- plogis(c(emp, vam))
}
cat("Belief in the theory after 20 tests: empirical ",
  round(100 * belief[21, 1]), "%, vampirical ",
  round(100 * belief[21, 2]), "%\n",
  sep = ""
)

matplot(0:20, belief, # <6>
  type = "l", lty = 1, lwd = 2, ylim = c(0, 1),
  col = c("#2166ac", "#d6604d"), xlab = "Tests of the theory",
  ylab = "Belief the theory is true"
)
legend("bottomleft", colnames(belief),
  col = c("#2166ac", "#d6604d"),
  lwd = 2, bty = "n"
)

# Annotations
# 1. The page's controls: how often a failed test is explained away, and how much evidence each failure carries.
# 2. Fixes the random numbers so the run is reproducible.
# 3. The theory is false, so tests mostly fail; an occasional false positive succeeds.
# 4. The empirical updater counts every test.
# 5. The vampirical updater counts the successes and explains away most failures, so the evidence never accumulates.
# 6. Belief in the theory over 20 tests. The empirical believer gives up; the vampire lives on.
