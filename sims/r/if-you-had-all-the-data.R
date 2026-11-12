# What would you do if you had all the data? Choosing the estimand.
heterogeneity <- 1.2 # variation in individual effects # <1>
self_select <- 0.6 # do people who benefit more choose treatment?
set.seed(55) # <2>

# Both potential outcomes, visible only in a simulation
y0 <- rnorm(3000)
effect <- 0.3 + heterogeneity * rnorm(3000)
y1 <- y0 + effect # <3>
chooses <- runif(3000) < 0.5 + self_select * tanh(effect) / 2 # <4>
randomized <- runif(3000) < 0.5

estimands <- c( # <5>
  "Average effect (everyone)" = mean(effect),
  "Effect on those who choose" = mean(effect[chooses]),
  "Median individual effect" = median(effect),
  "Share who benefit" = mean(effect > 0)
)
print(round(estimands, 2))
rct <- mean(y1[randomized]) - mean(y0[!randomized]) # <6>
cat(
  "A randomized experiment estimates", round(rct, 2),
  "(it targets the average effect)\n"
)

hist(effect, # <7>
  breaks = 50, col = "#2166ac", border = "white", main = "",
  xlab = "Individual treatment effect", ylab = "People"
)
abline(v = estimands[1:3], col = c("black", "#d6604d", "#b8860b"), lwd = 2)
abline(v = rct, lty = 2)

# Annotations
# 1. The page's controls: how much individual effects vary, and how strongly people who benefit more choose the treatment.
# 2. Fixes the random numbers so the run is reproducible.
# 3. With all the data, both potential outcomes are visible for everyone, which only a simulation allows.
# 4. Who would choose the treatment on their own.
# 5. Four different estimands you could want once you had all the data. They differ.
# 6. What a randomized experiment estimates: the average effect over everyone, whether or not that was the question.
# 7. The distribution of individual effects, with the estimands marked.
