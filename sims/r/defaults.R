# Defaults: one default prior scale for thousands of different problems.
spread <- 1 # typical effect size across users # <1>
set.seed(37) # <2>

tau <- spread * exp(rnorm(3000, 0, 0.7)) # each user's effect scale # <3>
se <- exp(rnorm(3000, -0.3, 0.6)) # each user's standard error
theta <- rnorm(3000, 0, tau)
y <- rnorm(3000, theta, se)
scales <- c(0.1, 0.2, 0.3, 0.5, 0.75, 1, 1.5, 2, 3, 5, 10, 100) # <4>
rmse <- sapply(scales, function(s) {
  w <- s^2 / (s^2 + se^2) # posterior mean under a N(0, s) default prior # <5>
  sqrt(mean((w * y - theta)^2))
})

cat(
  "Best default scale:", scales[which.min(rmse)], "(RMSE",
  round(min(rmse), 3), ")\n"
)
cat(
  "Flat 'no default' (scale 100): RMSE", round(rmse[length(rmse)], 3),
  "\n"
)

plot(scales, rmse, # <6>
  log = "x", type = "b", pch = 19, col = "#2166ac",
  xlab = "Default prior scale s (log scale)",
  ylab = "Average error across users (RMSE)"
)

# Annotations
# 1. The page's control: the typical effect size across the software's users.
# 2. Fixes the random numbers so the run is reproducible.
# 3. Three thousand users, each with a different effect scale and a different standard error.
# 4. Candidate default prior scales, from very tight to effectively flat.
# 5. Under a N(0, s) default prior, each user's estimate is shrunk by this factor.
# 6. Average error across all users for each default. A sensible default beats no default, and the flat prior is itself a default, just a bad one.
