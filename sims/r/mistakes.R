# Mistakes: admitting and learning from them lowers the error rate.
base_rate <- 0.25 # initial chance a project has an error # <1>
learning <- 0.2 # error-rate reduction per lesson learned
set.seed(96) # <2>

# Average cumulative mistakes over 200 careers of 50 projects each
run <- function(learns) { # <3>
  totals <- matrix(0, 200, 50)
  for (c in 1:200) {
    rate <- base_rate
    total <- 0
    for (t in 1:50) {
      if (runif(1) < rate) {
        total <- total + 1
        if (learns && runif(1) < 0.8) rate <- rate * (1 - learning) # <4>
      }
      totals[c, t] <- total
    }
  }
  colMeans(totals)
}
learns <- run(TRUE)
denies <- run(FALSE)
cat("Mistakes after 50 projects: admits and learns ", round(learns[50], 1),
  ", denies and repeats ", round(denies[50], 1), "\n",
  sep = ""
)

matplot(1:50, cbind(learns, denies), # <5>
  type = "l", lty = 1, lwd = 2,
  col = c("#2166ac", "#d6604d"), xlab = "Project",
  ylab = "Cumulative mistakes (average career)"
)
legend("topleft", c("Admits and learns", "Denies and repeats"),
  col = c("#2166ac", "#d6604d"), lwd = 2, bty = "n"
)

# Annotations
# 1. The page's controls: the initial chance that a project has an error, and how much each admitted mistake lowers it.
# 2. Fixes the random numbers so the run is reproducible.
# 3. Two hundred careers of 50 projects each, for a researcher who admits mistakes or one who denies them.
# 4. Admitting a mistake usually turns it into a lesson that lowers the error rate. Denying it leaves the rate where it was.
# 5. Cumulative mistakes over a career under the two habits.
