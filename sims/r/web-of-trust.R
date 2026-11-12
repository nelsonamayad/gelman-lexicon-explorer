# Web of Trust: more checks catch more bugs, unless they share blind spots.
p_catch <- 0.4 # power of each check # <1>
shared <- 0 # correlation between checks (shared blind spots)
set.seed(106) # <2>

K <- 0:8
missed <- sapply(K, function(k) {
  mean(replicate(4000, {
    blind <- runif(1) < shared # the bug is in a common blind spot # <3>
    !any(!blind & runif(k) < p_catch) # <4>
  }))
})
cat("Share of bugs that get through: 1 check ", round(100 * missed[2]),
  "%, 5 checks ", round(100 * missed[6]), "%, 8 checks ",
  round(100 * missed[9], 1), "%\n",
  sep = ""
)

plot(K, missed, # <5>
  type = "b", pch = 19, col = "#2166ac", ylim = c(0, 1),
  xlab = "Number of independent checks", ylab = "Share of bugs missed"
)
lines(K, (1 - p_catch)^K, lty = 2)

# Annotations
# 1. The page's controls: the power of each check and how much the checks share blind spots.
# 2. Fixes the random numbers so the run is reproducible.
# 3. Some bugs sit in a blind spot that every check shares.
# 4. A bug gets through if no check catches it.
# 5. The share of bugs missed against the number of checks, with the independent-checks curve dashed. Each weak strand helps, as long as the strands are independent.
