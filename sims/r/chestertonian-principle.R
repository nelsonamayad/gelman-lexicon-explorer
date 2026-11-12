# The Chestertonian Principle: extreme skepticism is a form of credulity.
survey_bias <- 0.08 # survey bias, known in direction and correctable # <1>
alt_bias <- 0.12 # spread of the alternative source's unknown bias
set.seed(65) # <2>

truth <- runif(500, 0.1, 0.9) # 500 questions about attitudes
survey <- truth - survey_bias * rnorm(500, 1, 0.3) + rnorm(500, 0, 0.03) # <3>
corrected <- survey + survey_bias # model-based correction # <4>
alternative <- truth + rnorm(500, 0, alt_bias) + rnorm(500, 0, 0.03) # <5>

rmse <- sapply( # <6>
  list(
    "Trusts raw survey" = survey,
    "Corrects survey biases" = corrected,
    "Extreme skeptic" = alternative
  ),
  function(est) sqrt(mean((est - truth)^2))
)
print(round(rmse, 3))

par(mar = c(4, 11, 1, 1))
barplot(rev(rmse),
  horiz = TRUE, las = 1,
  col = c("#d6604d", "#2166ac", "grey70"),
  xlab = "Root-mean-square error"
)

# Annotations
# 1. The page's controls: the survey's bias, whose direction is known, and the spread of the alternative source's unknown bias.
# 2. Fixes the random numbers so the run is reproducible.
# 3. Five hundred survey estimates, each biased downward by roughly the known amount.
# 4. The modeler's move: correct the known bias and accept what is left.
# 5. The extreme skeptic rejects the survey and trusts another source whose bias is unknown and goes either way.
# 6. Root-mean-square error of the three strategies. Rejecting a flawed-but-understood source for an unknown one is credulity, not skepticism.
