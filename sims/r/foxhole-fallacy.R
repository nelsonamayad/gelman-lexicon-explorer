# The Foxhole Fallacy: selective memory turns two-way traffic one-way.
to_mine <- 0.05 # true rate of switching to my method # <1>
from_mine <- 0.05 # true rate of switching away
memory_bias <- 0.8 # memory selectivity
set.seed(30) # <2>

# 500 practitioners use my method and 500 don't
to <- runif(500) < to_mine # <3>
away <- runif(500) < from_mine
to_remembered <- to & runif(500) < 0.5 + memory_bias / 2 # <4>
away_remembered <- away & runif(500) < 0.5 - memory_bias / 2

counts <- rbind(
  "Actually happened" = c(sum(to), sum(away)),
  "What I remember" = c(
    sum(to_remembered),
    sum(away_remembered)
  )
)
colnames(counts) <- c("Switched to my side", "Switched away")
print(counts)

barplot(t(counts), # <5>
  beside = TRUE, col = c("#2166ac", "#d6604d"),
  ylab = "Practitioners", legend.text = TRUE,
  args.legend = list(bty = "n")
)

# Annotations
# 1. The page's controls: the true rates of switching to and away from my method, and how selective my memory is.
# 2. Fixes the random numbers so the run is reproducible.
# 3. What actually happens: equal traffic in both directions.
# 4. What I remember: conversions to my side stick, defections fade.
# 5. Actual against remembered counts. Selective memory turns two-way traffic into a one-way street.
