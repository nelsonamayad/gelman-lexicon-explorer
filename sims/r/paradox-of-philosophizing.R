# The Paradox of Philosophizing: what share of discoveries are false?
pi_true <- 0.1 # share of tested hypotheses that are true # <1>
power <- 0.4 # power of each study
set.seed(36) # <2>

shift <- qnorm(0.975) + qnorm(power) # effect (in se units) with that power # <3>
real <- runif(5000) < pi_true
z <- rnorm(5000, ifelse(real, shift, 0), 1)
sig <- abs(z) > 1.96 # <4>
theory <- 0.05 * (1 - pi_true) / (0.05 * (1 - pi_true) + power * pi_true) # <5>

cat(sum(sig), " significant results, ", sum(sig & !real),
  " of them false (", round(100 * mean(!real[sig])), "%; theory ",
  round(100 * theory), "%)\n",
  sep = ""
)

barplot( # <6>
  c(
    "True discoveries" = sum(sig & real),
    "False discoveries" = sum(sig & !real)
  ),
  col = c("#2166ac", "#d6604d"), ylab = "Significant results"
)

# Annotations
# 1. The page's controls: the share of tested hypotheses that are true, and the power of each study.
# 2. Fixes the random numbers so the run is reproducible.
# 3. The effect size that gives a true hypothesis the chosen power.
# 4. The philosophy-free rule: declare a discovery when p < 0.05.
# 5. The share of discoveries that are false, from Bayes' rule. The rule's meaning depends on the base rate the analyst refused to state.
# 6. True and false discoveries. The analyst who declined to philosophize chose a prior anyway.
