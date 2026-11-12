# The Australia principle: build the prior where the likelihood is weak.
n <- 3000 # survey sample size # <1>
set.seed(75) # <2>

posterior <- function(prior_mean, prior_sd, est, se) { # <3>
  w0 <- 1 / prior_sd^2
  w1 <- 1 / se^2
  m <- (w0 * prior_mean + w1 * est) / (w0 + w1)
  s <- sqrt(1 / (w0 + w1))
  c(mean = m, lo = m - 1.96 * s, hi = m + 1.96 * s)
}
# Q1: an opinion proportion (truth 0.52); effects of interest ~5 points
se1 <- 0.5 / sqrt(n) # <4>
est1 <- 0.52 + rnorm(1, 0, se1)
# Q2: difference in Pr(girl) between two groups (truth 0.002)
se2 <- sqrt(2 * 0.25 / (n / 2)) # <5>
est2 <- 0.002 + rnorm(1, 0, se2)

res <- 100 * rbind( # <6>
  "Q1, vague prior"       = posterior(0.5, 1, est1, se1),
  "Q1, informative prior" = posterior(0.5, 0.05, est1, se1),
  "Q2, vague prior"       = posterior(0, 1, est2, se2),
  "Q2, informative prior" = posterior(0, 0.003, est2, se2)
)
print(round(res, 2)) # in percentage points
cat(
  "Q2 standard error:", round(100 * se2, 2),
  "points, against a true effect of 0.2 points\n"
)

par(mfrow = c(2, 1), mar = c(4, 11, 2, 1))
for (q in c("Q1", "Q2")) {
  r <- res[startsWith(rownames(res), q), ]
  plot(r[, "mean"], 1:2,
    xlim = range(r), ylim = c(0.5, 2.5), pch = 19,
    yaxt = "n", ylab = "", xlab = "Percentage points", main = q
  )
  segments(r[, "lo"], 1:2, r[, "hi"], 1:2,
    lwd = 3,
    col = c("#d6604d", "#2166ac")
  )
  axis(2, 1:2, c("Vague prior", "Informative prior"), las = 1)
  abline(v = if (q == "Q1") 52 else 0.2, lty = 2)
}

# Annotations
# 1. The page's control: the survey sample size.
# 2. Fixes the random numbers so the run is reproducible.
# 3. The conjugate normal update: a prior and an estimate with its standard error give a posterior mean and 95% interval.
# 4. Question 1, an opinion proportion. The data are precise relative to the effects of interest, so the prior hardly matters.
# 5. Question 2, a tiny difference in the probability of a girl. The data are far too noisy, so the prior does all the work. That is the Australia principle: build the prior where the likelihood is weak.
# 6. The four posteriors in percentage points: each question with a vague and with an informative prior.
