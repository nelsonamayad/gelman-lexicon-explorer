# A chicken: Bill James's check of a fielding rating, in miniature.
adjust <- FALSE # FALSE: rate by raw assists; TRUE: adjust for team # <1>
gb_effect <- 0.8 # how much team ground balls drive assists
set.seed(118) # <2>

gb <- rep(rnorm(30), each = 2) # team ground-ball tendency, 2 per team
skill <- rnorm(60) # fielders' true skill
assists <- 300 + 15 * skill + 40 * gb_effect * gb + rnorm(60, 0, 10) # <3>
score <- if (adjust) resid(lm(assists ~ gb)) else assists # <4>
rating <- as.vector(scale(score))

top10 <- order(rating, decreasing = TRUE)[1:10] # <5>
cut <- sort(gb, decreasing = TRUE)[20] # top third of fielders by team
cat("Top-10 fielders on ground-ball teams:", sum(gb[top10] >= cut), "of 10\n")
cat("Correlation with team ground balls:", round(cor(rating, gb), 2), "\n")
cat("Correlation with true skill:", round(cor(rating, skill), 2), "\n")

plot(gb, rating, # <6>
  pch = 19, col = "#2166ac",
  xlab = "Team ground-ball tendency (sd units)",
  ylab = "Fielder rating (sd units)"
)
abline(lm(rating ~ gb), col = "#d6604d", lwd = 2)
abline(h = 0)

# Annotations
# 1. The page's controls: whether to adjust for the team's ground balls, and how much those ground balls drive assists.
# 2. Fixes the random numbers so the run is reproducible.
# 3. A fielder's assists depend on his skill and on how many ground balls his pitchers give up: the chance factor Total Baseball ignored.
# 4. The two models. Raw assists, as Total Baseball did, or assists after regressing out the team's ground-ball tendency.
# 5. The posterior check: do the ten top-rated fielders all happen to play for ground-ball teams? Skill is unrelated to team, so they shouldn't.
# 6. Each fielder's rating against his team's ground-ball tendency. A sloping line is the absurd inference Bill James noticed.
