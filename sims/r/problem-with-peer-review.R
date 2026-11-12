# The problem with peer review: more reviewers don't catch shared errors.
p_catch <- 0.5 # reviewer skill: chance of catching an error they see # <1>
m <- 0.85 # share of the field sharing the misconception
set.seed(61) # <2>

reviewers <- c(1, 2, 3, 4, 5, 6, 8, 10)
caught <- sapply(reviewers, function(k) {
  hit <- function(shared) {
    replicate(2000, {
      blind <- shared & runif(k) < m # this reviewer shares the error # <3>
      any(!blind & runif(k) < p_catch) # <4>
    })
  }
  c(idiosyncratic = mean(hit(FALSE)), shared = mean(hit(TRUE)))
})
cat("With 10 reviewers: an idiosyncratic error is caught ",
  round(100 * caught[1, 8]), "% of the time, a shared misconception ",
  round(100 * caught[2, 8]), "%\n",
  sep = ""
)

matplot(reviewers, t(caught), # <5>
  type = "b", pch = 19, lty = 1,
  ylim = c(0, 1), col = c("#2166ac", "#d6604d"),
  xlab = "Number of reviewers", ylab = "Share of errors caught"
)
legend("right", c("Idiosyncratic error", "Shared misconception"),
  col = c("#2166ac", "#d6604d"), pch = 19, bty = "n"
)

# Annotations
# 1. The page's controls: a reviewer's skill at catching errors they can see, and the share of the field that shares the misconception.
# 2. Fixes the random numbers so the run is reproducible.
# 3. For a shared misconception, each reviewer is probably blind to it, because they are a peer.
# 4. The error is caught if any reviewer both sees it and catches it.
# 5. Detection against the number of reviewers. Adding peers helps with idiosyncratic errors and barely at all with the one they all share.
