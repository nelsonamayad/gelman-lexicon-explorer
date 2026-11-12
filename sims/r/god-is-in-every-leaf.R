# God is in every leaf of every tree: missing answers coded as 99.
miss_rate <- 0.04 # share of responses missing # <1>
missing_related <- TRUE # missingness more common among older respondents
set.seed(27) # <2>

age <- runif(1000, 18, 80)
rating <- round(6 - 0.03 * (age - 50) + rnorm(1000, 0, 1.8))
rating <- pmin(10, pmax(1, rating)) # a 1-10 scale
p_miss <- if (missing_related) miss_rate * 2 * (age - 18) / 62 else miss_rate # <3>
missing <- runif(1000) < p_miss
recorded <- ifelse(missing, 99, rating) # the "trivial" coding detail # <4>

cat(
  "Mean rating: 99 treated as a number", round(mean(recorded), 2),
  "| missing code dropped", round(mean(rating[!missing]), 2), "\n"
)
cat(
  "Slope on age:", round(coef(lm(recorded ~ age))[2], 3), "vs",
  round(coef(lm(rating[!missing] ~ age[!missing]))[2], 3), "\n"
)

plot(age, recorded, # <5>
  log = "y", pch = 16, cex = 0.6,
  col = ifelse(missing, "#d6604d", "#2166ac"), xlab = "Age",
  ylab = "Recorded rating (log scale)"
)

# Annotations
# 1. The page's controls: the share of missing responses, and whether missingness rises with age.
# 2. Fixes the random numbers so the run is reproducible.
# 3. Older respondents skip the question more often, so the missing code is not spread evenly.
# 4. The trivial coding detail: missing answers stored as 99 on a 1 to 10 scale.
# 5. Recorded ratings against age. The 99s sit far above the scale and, being concentrated among the old, flip the slope on age.
