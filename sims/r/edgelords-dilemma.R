# The Edgelord's Dilemma: who stands near you far from the consensus?
my_pos <- 2.2 # your distance from consensus (sd units) # <1>
bad_share <- 0.05 # bad-faith actors as a share of everyone
set.seed(148) # <2>

N <- 10000
n_bad <- round(N * bad_share)
careful <- rnorm(N - n_bad) # careful thinkers # <3>
bad <- sample(c(-1, 1), n_bad, replace = TRUE) * rnorm(n_bad, 3, 0.7) # <4>
near_careful <- sum(abs(careful - my_pos) < 0.25)
near_bad <- sum(abs(bad - my_pos) < 0.25) # <5>

cat("Near you: ", near_bad, " bad-faith actors and ", near_careful,
  " careful thinkers (", round(100 * near_bad / (near_bad + near_careful)),
  "% bad faith)\n",
  sep = ""
)

breaks <- seq(-7, 7, by = 0.25)
h1 <- hist(careful[abs(careful) < 7], breaks = breaks, plot = FALSE)
h2 <- hist(bad[abs(bad) < 7], breaks = breaks, plot = FALSE)
barplot(rbind(h1$counts, h2$counts), # <6>
  col = c("#2166ac", "#d6604d"),
  border = NA, space = 0, names.arg = round(h1$mids, 1),
  xlab = "Position (sd units from consensus)", ylab = "People"
)
legend("topright", c("Careful thinkers", "Bad-faith actors"),
  fill = c("#2166ac", "#d6604d"), bty = "n"
)

# Annotations
# 1. The page's controls: how far from the consensus you stand, and what share of everyone argues in bad faith.
# 2. Fixes the random numbers so the run is reproducible.
# 3. Careful thinkers cluster near the consensus.
# 4. Bad-faith actors cluster far from it, on both sides.
# 5. Who else stands where you stand.
# 6. The two distributions. Far from the consensus, your neighbors are mostly the people you would least like to be mistaken for.
