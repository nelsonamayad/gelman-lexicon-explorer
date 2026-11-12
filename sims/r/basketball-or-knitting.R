# Basketball, or knitting: judging scatterplots is learned by practice.
true_r <- 0.4 # correlation when the pattern is real # <1>
lr <- 0.01 # how quickly feedback adjusts judgment
set.seed(98) # <2>

real <- runif(300) < 0.5
r_obs <- sapply(real, function(is_real) { # <3>
  rho <- if (is_real) true_r else 0
  x <- rnorm(20)
  abs(cor(x, rho * x + sqrt(1 - rho^2) * rnorm(20)))
})
threshold <- 0.05 # the learner starts by seeing patterns everywhere
rules <- 0.05 # the rules-only learner never adjusts
feedback_ok <- rules_ok <- logical(300)
for (i in 1:300) {
  says <- r_obs[i] > threshold
  feedback_ok[i] <- says == real[i]
  rules_ok[i] <- (r_obs[i] > rules) == real[i] # <5>
  if (says != real[i]) threshold <- threshold + if (says) lr else -lr # <4>
}

cat("Accuracy in the last 100 judgments: with feedback ",
  round(100 * mean(feedback_ok[201:300])), "%, rules only ",
  round(100 * mean(rules_ok[201:300])), "% (chance: 50%)\n",
  sep = ""
)

block <- rep(1:15, each = 20)
acc <- cbind(tapply(feedback_ok, block, mean), tapply(rules_ok, block, mean))
matplot(1:15, acc, # <6>
  type = "b", pch = 19, lty = 1, ylim = c(0, 1),
  col = c("#2166ac", "#d6604d"), xlab = "Block of 20 judgments",
  ylab = "Accuracy"
)
abline(h = 0.5, lty = 2)
legend("bottomright", c("Practice with feedback", "Read the rules only"),
  col = c("#2166ac", "#d6604d"), pch = 19, bty = "n"
)

# Annotations
# 1. The page's controls: the correlation when a pattern is real, and how fast feedback adjusts the learner's judgment.
# 2. Fixes the random numbers so the run is reproducible.
# 3. Three hundred scatterplots of 20 points, half with a real correlation and half pure noise. The learner sees only the sample correlation.
# 4. Practice with feedback: after each wrong call the learner moves the threshold for calling a pattern real.
# 5. The rules-only learner keeps the threshold the textbook gave and never adjusts it.
# 6. Accuracy in blocks of 20 judgments. Practice improves; reading the rules does not.
