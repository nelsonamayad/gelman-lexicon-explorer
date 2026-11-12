# Steelmanning: adopting X's framing of Y biases your view of Y.
w <- 0.6 # how much the observer adopts X's framing # <1>
exag <- 1 # how much X caricatures Y
set.seed(142) # <2>

q_Y <- rnorm(500) # true quality of Y's work
direct <- q_Y + rnorm(500, 0, 0.5) # the observer's own look
x_account <- q_Y - exag + rnorm(500, 0, 0.5) # X's description of Y # <3>
view <- (1 - w) * direct + w * x_account # <4>
cat(
  "On average the observer rates Y's work", round(mean(view - q_Y), 2),
  "relative to its true quality\n"
)

plot(q_Y, view, # <5>
  pch = 19, cex = 0.5, col = "#d6604d",
  xlab = "True quality of Y's work", ylab = "Observer's view"
)
abline(0, 1, lty = 2)

# Annotations
# 1. The page's controls: how much the observer adopts X's framing of Y, and how much X caricatures Y.
# 2. Fixes the random numbers so the run is reproducible.
# 3. X's account of Y's work: systematically worse than it is.
# 4. The observer's view: a mix of their own look and X's account. Steelmanning X means weighting X's framing.
# 5. The observer's view against Y's true quality. Bending over backward for X means being unfair to Y.
