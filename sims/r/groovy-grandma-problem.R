# The Groovy Grandma Problem: weighting fixes the age mix, not grooviness.
groovy <- 2.5 # how much grooviness boosts response among older people # <1>
set.seed(149) # <2>

N <- 60000
old <- rbinom(N, 1, 0.4)
g <- rbinom(N, 1, ifelse(old == 1, 0.15, 0.5)) # "groovy" # <3>
support <- rbinom(N, 1, 0.35 + 0.3 * g - 0.1 * old)
resp <- runif(N) < plogis(-3 + ifelse(old == 1, -1 + groovy * g, 0.5 * g)) # <4>

cell <- function(o) mean(support[resp & old == o])
weighted <- 0.4 * cell(1) + 0.6 * cell(0) # weighted to the census age mix # <5>
cat("Groovy among older respondents: ",
  round(100 * mean(g[resp & old == 1])), "% (15% in the population)\n",
  sep = ""
)
cat("Truth: ", round(100 * mean(support), 1), "% | weighted estimate: ",
  round(100 * weighted, 1), "%\n",
  sep = ""
)

est <- c(
  Truth = mean(support), "Raw sample" = mean(support[resp]),
  "Weighted by age" = weighted
)
dotchart(100 * est, # <6>
  pch = 19, col = c("black", "#d6604d", "#d6604d"),
  xlab = "Support (%)"
)

# Annotations
# 1. The page's control: how much being groovy raises an older person's chance of answering the survey.
# 2. Fixes the random numbers so the run is reproducible.
# 3. Grooviness is rare among the old and common among the young, and it predicts the outcome.
# 4. Who responds: older people rarely, unless they are groovy.
# 5. Weighting fixes the age mix, but the older respondents are still the groovy ones.
# 6. The truth, the raw sample and the weighted estimate. The weights adjusted for the wrong variable.
