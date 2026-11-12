# Reverse Poe: sincere work so absurd that readers take it for parody.
tail <- 0.08 # share of sincere papers with absurd claims # <1>
threshold <- 3 # reader's "must be a joke" threshold
set.seed(63) # <2>

# Absurdity score of 2000 sincere papers and 300 parodies
sincere <- ifelse(runif(2000) < tail, rnorm(2000, 4, 0.8), # <3>
  rnorm(2000, 1, 0.8)
)
parody <- rnorm(300, 4.2, 0.8) # <4>
rp <- sum(sincere > threshold) # <5>
cat(rp + sum(parody > threshold), " texts look like jokes; ", rp,
  " of them (", round(100 * rp / (rp + sum(parody > threshold))),
  "%) are sincere\n",
  sep = ""
)

breaks <- seq(-3, 8, by = 0.25)
hist(sincere, # <6>
  breaks = breaks, col = adjustcolor("#2166ac", 0.6),
  border = "white", main = "", xlab = "Absurdity score",
  ylab = "Texts"
)
hist(parody,
  breaks = breaks, col = adjustcolor("#d6604d", 0.6),
  border = "white", add = TRUE
)
abline(v = threshold, lty = 2)
legend("topright", c("Sincere", "Parody"),
  fill = c("#2166ac", "#d6604d"),
  bty = "n"
)

# Annotations
# 1. The page's controls: the share of sincere papers with absurd claims, and the absurdity at which a reader decides it must be a joke.
# 2. Fixes the random numbers so the run is reproducible.
# 3. Sincere papers, most of them ordinary, a tail of them absurd.
# 4. Parodies, which are absurd by design.
# 5. The reverse Poes: sincere papers absurd enough to be taken for parody.
# 6. Absurdity scores of sincere work and parody. Where the distributions overlap, the reader cannot tell them apart.
