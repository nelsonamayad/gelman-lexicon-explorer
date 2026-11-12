# The "What does not kill my statistical significance makes it stronger"
# fallacy: significance found through noise is weaker evidence.
theta <- 0.2 # true effect # <1>
set.seed(62) # <2>

ses <- c(0.05, 0.1, 0.15, 0.2, 0.3, 0.4, 0.5, 0.75, 1) # <3>
res <- t(sapply(ses, function(se) {
  e <- rnorm(20000, theta, se)
  sig <- e[abs(e) > 1.96 * se] # the significant estimates # <4>
  c(
    se = se, power = length(sig) / 20000,
    exaggeration = mean(abs(sig)) / theta, wrong_sign = mean(sig < 0)
  )
}))
print(round(res, 3))

plot(res[, "se"], res[, "exaggeration"], # <5>
  type = "b", pch = 19,
  col = "#d6604d", xlab = "Standard error (noise)",
  ylab = "Exaggeration of significant estimates"
)
abline(h = 1, lty = 2)

# Annotations
# 1. The page's control: the true effect.
# 2. Fixes the random numbers so the run is reproducible.
# 3. Studies of increasing noisiness.
# 4. The significant estimates at each noise level.
# 5. How much the significant estimates exaggerate the truth as the noise grows. Significance that survived more noise is weaker evidence, not stronger.
