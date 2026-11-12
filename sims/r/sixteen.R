# 16: you need 16 times the sample size to estimate an interaction.
theta <- 0.4 # main effect (in sd units) # <1>
int_ratio <- 0.5 # interaction as a fraction of the main effect
set.seed(80) # <2>

ns <- c(10, 20, 40, 80, 160, 320, 640, 1280) # people per cell
gamma <- int_ratio * theta # <3>
power <- sapply(ns, function(n) {
  hits <- replicate(400, {
    # Cells (treatment a, group b); main effect theta, interaction gamma
    cell <- function(a, b) { # <4>
      mean(rnorm(n, theta * (a - 0.5) +
        gamma * (a - 0.5) * (b - 0.5), 1))
    }
    m00 <- cell(0, 0)
    m10 <- cell(1, 0)
    m01 <- cell(0, 1)
    m11 <- cell(1, 1)
    main <- ((m10 - m00) + (m11 - m01)) / 2 # <5>
    inter <- (m11 - m01) - (m10 - m00) # <6>
    c(main = abs(main * sqrt(n)) > 1.96, inter = abs(inter * sqrt(n) / 2) >
      1.96)
  })
  rowMeans(hits)
})
z <- qnorm(0.975) + qnorm(0.8) # <7>
cat("People per cell for 80% power: main effect ", ceiling(z^2 / theta^2),
  ", interaction ", ceiling(z^2 * 4 / gamma^2), "\n",
  sep = ""
)

matplot(ns, t(power), # <8>
  type = "b", pch = 19, lty = 1, log = "x",
  col = c("#2166ac", "#d6604d"), ylim = c(0, 1),
  xlab = "People per cell", ylab = "Power"
)
abline(h = 0.8, lty = 2)
legend("topleft", c("Main effect", "Interaction"),
  col = c("#2166ac", "#d6604d"), pch = 19, bty = "n"
)

# Annotations
# 1. The page's controls: the main effect and the interaction as a fraction of it.
# 2. Fixes the random numbers so the run is reproducible.
# 3. The interaction: half the main effect by default.
# 4. A cell mean of a 2 by 2 design with n people per cell, coded plus or minus one half, so the interaction is the difference of differences.
# 5. The main effect estimate, with standard error 1 over the square root of n.
# 6. The interaction estimate, with twice that standard error.
# 7. The analytic answer: half the effect with twice the standard error is a quarter of the z-score, so 16 times the sample.
# 8. Power against people per cell for both. The interaction's curve is the main effect's shifted 16-fold to the right.
