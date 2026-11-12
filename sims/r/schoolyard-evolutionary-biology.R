# Schoolyard Evolutionary Biology: a group difference amid individual
# variation.
d <- 0.3 # average group difference (Cohen's d) # <1>
set.seed(107) # <2>

a <- rnorm(3000, 0, 1)
b <- rnorm(3000, d, 1) # <3>
cat("Overlap of the two distributions: ", round(100 * 2 * pnorm(-d / 2)),
  "%\nA random B exceeds a random A ", round(100 * pnorm(d / sqrt(2))),
  "% of the time (simulated: ",
  round(100 * mean(sample(b) > sample(a))), "%)\n", # <4>
  "Variance explained by group: ", round(100 * d^2 / (d^2 + 4), 1),
  "%\n",
  sep = ""
)

breaks <- seq(-5, 6, by = 0.2)
hist(a, # <5>
  breaks = breaks, col = adjustcolor("#2166ac", 0.5),
  border = "white", main = "", xlab = "Trait", ylab = "People"
)
hist(b,
  breaks = breaks, col = adjustcolor("#d6604d", 0.5),
  border = "white", add = TRUE
)
legend("topright", c("Group A", "Group B"),
  fill = c("#2166ac", "#d6604d"),
  bty = "n"
)

# Annotations
# 1. The page's control: the average difference between the groups, in standard deviations.
# 2. Fixes the random numbers so the run is reproducible.
# 3. Two groups whose means differ by d, with the same individual variation.
# 4. How often a random member of one group exceeds a random member of the other: barely more than a coin flip for a typical d.
# 5. The two distributions overlap almost entirely. A group difference says little about any two individuals.
