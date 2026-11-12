# That toothpaste feeling: jargon makes weak explanations feel better.
tingle <- 1 # jargon boost to ratings # <1>
set.seed(92) # <2>

jargon <- rep(c(TRUE, FALSE), 1000)
quality <- rnorm(2000)
good <- quality > 0
boost <- ifelse(jargon, tingle * ifelse(good, 0.4, 1), 0) # weak gain more # <3>
rating <- 4 + quality + boost + rnorm(2000, 0, 0.5)
correct <- runif(2000) < ifelse(good, 0.85, 0.3) # <4>

g <- interaction(ifelse(good, "Good", "Bad"),
  ifelse(jargon, "jargon", "plain"),
  sep = ", "
)
print(round(cbind(
  rating = tapply(rating, g, mean),
  accuracy = tapply(correct, g, mean)
), 2))

boxplot(rating ~ g, # <5>
  col = c("#d6604d", "#2166ac"), xlab = "",
  ylab = "Rating of the explanation"
)

# Annotations
# 1. The page's control: how much the jargon boosts ratings.
# 2. Fixes the random numbers so the run is reproducible.
# 3. Jargon raises ratings, and weak explanations gain the most from it.
# 4. Whether the explanation is actually right depends on its quality, not its jargon.
# 5. Ratings by quality and by jargon. The tingle is not the clean.
