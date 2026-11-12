# Canary variable: a known quantity that warns of hidden selection.
hidden <- 1 # strength of hidden selection # <1>
canary_link <- 0.7 # canary's correlation with the hidden trait
set.seed(117) # <2>

population <- function(n) { # <3>
  old <- rbinom(n, 1, 0.5)
  u <- rnorm(n) # u: trait we can't adjust for
  data.frame(old, u,
    target = rbinom(n, 1, plogis(-0.2 + 0.4 * old + 0.8 * u)),
    canary = rbinom(n, 1, plogis(canary_link * 1.5 * u + 0.3 * old))
  )
}
truth <- colMeans(population(40000)[, c("target", "canary")])

errors <- t(replicate(200, {
  h <- hidden * runif(1, 0.2, 1.2) # selection strength varies by survey
  d <- population(4000)
  resp <- d[runif(4000) < plogis(-2 + 0.8 * d$old + h * d$u), ] # <4>
  w <- ifelse(resp$old == 1, 0.5 / mean(resp$old), 0.5 / mean(1 - resp$old)) # <5>
  c(
    canary = weighted.mean(resp$canary, w) - truth[["canary"]],
    target = weighted.mean(resp$target, w) - truth[["target"]]
  )
}))

cat(
  "Correlation of canary error with target error:",
  round(cor(errors[, "canary"], errors[, "target"]), 2), "\n"
)
cat(
  "Average target error after weighting:",
  round(mean(errors[, "target"]), 3), "\n"
)

plot(errors[, "canary"], errors[, "target"], # <6>
  pch = 19, col = "#2166ac",
  xlab = "Canary's error after weighting",
  ylab = "Target's error after weighting"
)
abline(h = 0, v = 0, lty = 2)

# Annotations
# 1. The page's controls: how strongly a hidden trait drives survey response, and how closely the canary variable tracks that trait.
# 2. Fixes the random numbers so the run is reproducible.
# 3. A population with age, a hidden trait, the target outcome and the canary. The canary's true population value is known from outside.
# 4. Who responds depends on age, which we adjust for, and on the hidden trait, which we can't.
# 5. Weight the respondents so the age mix matches the population. This fixes age and nothing else.
# 6. Across 200 surveys, the canary's error after weighting against the target's. When the canary is off, the target is off too.
