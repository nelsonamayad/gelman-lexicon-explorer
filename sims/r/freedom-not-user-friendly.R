# Freedom: it's not user friendly.
skill <- 0.5 # average analyst skill # <1>
set.seed(102) # <2>

s <- pmin(1, pmax(0, rnorm(2000, skill, 0.2))) # each analyst
constrained <- 0.65 + rnorm(2000, 0, 0.05) # good defaults, limited ceiling # <3>
free <- pmax(-0.5, 0.95 - (1 - s) * abs(rnorm(2000, 0, 0.6))) # skill-bound # <4>

q <- rbind(
  constrained = quantile(constrained, c(0.1, 0.5)),
  free = quantile(free, c(0.1, 0.5))
)
print(round(q, 2)) # worst 10% and median quality

boxplot( # <5>
  list(
    "Constrained, user-friendly" = constrained,
    "Free, flexible" = free
  ),
  col = c("#2166ac", "#d6604d"), ylab = "Quality of the analysis"
)

# Annotations
# 1. The page's control: the average skill of the analysts.
# 2. Fixes the random numbers so the run is reproducible.
# 3. A constrained, user-friendly tool: good defaults, a limited ceiling, hard to misuse.
# 4. A free, flexible tool: a higher ceiling, but the floor depends on the analyst's skill.
# 5. The two distributions of analysis quality. Freedom raises the best outcomes and lowers the worst.
