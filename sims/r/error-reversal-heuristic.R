# The Error-Reversal Heuristic: checking harder when errors hurt the story.
p_conv <- 0.2 # chance of catching an error that helps the story # <1>
p_inconv <- 0.8 # chance of catching an error that hurts the story
set.seed(144) # <2>

est <- rnorm(3000, 0, 0.2) # the true effect is zero
has_err <- runif(3000) < 0.3
err <- ifelse(has_err, rnorm(3000, 0, 0.6), 0) # <3>
caught <- has_err & runif(3000) < ifelse(err > 0, p_conv, p_inconv) # <4>
published <- est + ifelse(caught, 0, err) # <5>

cat(
  "Average published estimate:", round(mean(published), 3),
  "(true effect: 0)\n"
)

breaks <- seq(min(est, published) - 0.1, max(est, published) + 0.1,
  length.out = 60
)
hist(est, # <6>
  breaks = breaks, col = adjustcolor("#2166ac", 0.5),
  border = "white", main = "", xlab = "Estimate", ylab = "Studies"
)
hist(published,
  breaks = breaks, col = adjustcolor("#d6604d", 0.5),
  border = "white", add = TRUE
)
abline(v = 0, lwd = 2)
legend("topright", c("Honest estimates", "Published"),
  fill = adjustcolor(c("#2166ac", "#d6604d"), 0.5), bty = "n"
)

# Annotations
# 1. The page's controls: how likely an error is to be caught when it helps the story, and when it hurts it.
# 2. Fixes the random numbers so the run is reproducible.
# 3. Three thousand honest estimates of a zero effect; 30% of them contain an error that pushes either way.
# 4. Errors that hurt the story get caught; errors that help it mostly don't. That asymmetry is the whole mechanism.
# 5. What gets published: the honest estimate plus any error that survived.
# 6. Honest estimates against published ones. The published distribution has drifted away from zero without anyone intending it.
