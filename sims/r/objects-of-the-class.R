# Objects of the class: broad, narrow, or partially pooled reference class.
n_narrow <- 12 # members of the narrow class # <1>
gap_rate <- 0.2 # how different the narrow class really is
set.seed(141) # <2>

p_broad <- 0.35
p_med <- p_broad + gap_rate / 2
p_narrow <- p_broad + gap_rate # the rate we want to estimate # <3>
est <- replicate(2000, {
  broad <- rbinom(1, 3000, p_broad) / 3000
  medium <- rbinom(1, 300, p_med) / 300
  narrow <- rbinom(1, n_narrow, p_narrow) / n_narrow # <4>
  w <- n_narrow / (n_narrow + 25) # shrink the narrow class toward medium # <5>
  c(
    Broad = broad, Medium = medium, Narrow = narrow,
    "Partial pooling" = w * narrow + (1 - w) * medium
  )
})
rmse <- sqrt(rowMeans((est - p_narrow)^2))
print(round(rmse, 3)) # error in estimating the narrow class's rate

barplot(rmse, # <6>
  col = c("grey70", "grey70", "grey70", "#2166ac"),
  ylab = "Root mean squared error"
)

# Annotations
# 1. The page's controls: how many members the narrow reference class has, and how different it really is from the broad one.
# 2. Fixes the random numbers so the run is reproducible.
# 3. The rate we want: the narrow class's.
# 4. The narrow class's observed rate is right on average but noisy, because the class is small.
# 5. Partial pooling: shrink the narrow class's rate toward the medium class's, more when the narrow class is smaller.
# 6. Error of each reference class, and of partial pooling, which usually beats any single class.
