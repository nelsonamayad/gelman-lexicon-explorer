# Two sides, no vig: a theory that bets on both outcomes risks nothing.
true_effect <- 0 # true effect # <1>
set.seed(137) # <2>

z <- rnorm(30, true_effect / 0.2, 1) # 30 studies
noticed <- abs(z) > 1 # a "noticeable" result
committed_conf <- cumsum(noticed & z > 0) # predicted positive # <3>
two_sided_conf <- cumsum(noticed) # either sign "confirms" it # <4>
# Evidence for the committed theory: it predicts a positive result with
# probability 0.8, against 0.5 with no theory. The two-sided theory
# predicts both signs, so its evidence never moves from 50%.
lo <- cumsum(ifelse(noticed, ifelse(z > 0, log(0.8 / 0.5), # <5>
  log(0.2 / 0.5)
), 0))
cat("After 30 studies: 'confirmations' two-sided ", tail(two_sided_conf, 1),
  ", committed ", tail(committed_conf, 1), "\nProbability the theory is ",
  "right: two-sided 50%, committed ", round(100 * plogis(tail(lo, 1))),
  "%\n",
  sep = ""
)

par(mfrow = c(1, 2)) # <6>
matplot(1:30, cbind(two_sided_conf, committed_conf),
  type = "s", lty = 1,
  lwd = 2, col = c("#d6604d", "#2166ac"), xlab = "Study",
  ylab = "'Confirmations'"
)
plot(1:30, plogis(lo),
  type = "l", lwd = 2, col = "#2166ac",
  ylim = c(0, 1), xlab = "Study", ylab = "Probability theory is right"
)
abline(h = 0.5, col = "#d6604d", lwd = 2)

# Annotations
# 1. The page's control: the true effect, zero by default.
# 2. Fixes the random numbers so the run is reproducible.
# 3. The committed theory predicts a positive result, so only noticeable positive results count as confirmations.
# 4. The two-sided theory explains either sign, so every noticeable result confirms it.
# 5. The evidence, as a Bayesian would count it. The committed theory risks something and is rewarded or punished; the two-sided theory's likelihood ratio is always one.
# 6. Confirmations and the probability the theory is right. Counting confirmations flatters the theory that bet both ways.
