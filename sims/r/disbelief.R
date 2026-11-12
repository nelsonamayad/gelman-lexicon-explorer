# Disbelief remains an option: published results are selected results.
n_pub <- 8 # published significant studies # <1>
prior <- 0.1 # prior probability the effect is real
set.seed(103) # <2>

delta <- 2.5 # z-score shift if the effect were real
# The truth is no effect: published z-scores are draws above 1.96
z <- qnorm(runif(n_pub, pnorm(1.96), 1)) # <3>
lr_naive <- dnorm(z, delta) / dnorm(z, 0) # <4>
lr_aware <- (dnorm(z, delta) / (1 - pnorm(1.96 - delta))) / # <5>
  (dnorm(z, 0) / (1 - pnorm(1.96))) # conditions on selection
logit_prior <- qlogis(prior)
naive <- plogis(logit_prior + cumsum(log(lr_naive)))
aware <- plogis(logit_prior + cumsum(log(lr_aware)))

cat("After ", n_pub, " published studies, the naive reader is ",
  round(100 * tail(naive, 1), 1), "% convinced; the selection-aware ",
  "reader is ", round(100 * tail(aware, 1), 1), "%\n",
  sep = ""
)

matplot(0:n_pub, cbind(c(prior, naive), c(prior, aware)), # <6>
  type = "b",
  pch = 19, lty = 1, col = c("#d6604d", "#2166ac"), ylim = c(0, 1),
  xlab = "Published significant studies",
  ylab = "Probability the effect is real"
)
legend("right", c("Naive (no selection)", "Selection-aware"),
  col = c("#d6604d", "#2166ac"), pch = 19, bty = "n"
)

# Annotations
# 1. The page's controls: how many significant studies were published, and the reader's prior probability that the effect is real.
# 2. Fixes the random numbers so the run is reproducible.
# 3. The truth is no effect, yet every published z-score is above 1.96, because only significant results were published.
# 4. The naive reader's likelihood ratio for each study, as if the result could have come out either way.
# 5. The selection-aware reader's likelihood ratio, which conditions on the result being significant. Under selection, a significant result is almost equally likely either way.
# 6. Belief after each published study. The naive reader is convinced; the aware reader keeps disbelief as an option.
