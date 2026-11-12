# Scientific revolutions are fractal: power-law sizes look the same at
# every scale (a toy model).
alpha <- 1.2 # power-law exponent # <1>
set.seed(145) # <2>

sizes <- sort((1 - runif(5000))^(-1 / alpha), decreasing = TRUE) # <3>
sub <- sizes[sizes < 20] * 5 # zoom into a subfield, rescaled # <4>
ccdf <- function(s) (seq_along(s)) / length(s) # share at least this big
cat(
  sum(sizes > 100), "of 5000 changes are more than 100 times the",
  "minimum size\n"
)

plot(sizes, ccdf(sizes), # <5>
  log = "xy", type = "l", lwd = 2, col = "#2166ac",
  xlab = "Size of the change", ylab = "Share at least this big"
)
lines(sub, ccdf(sub), lwd = 2, col = "#d6604d", lty = 2)
legend("bottomleft", c("All of science", "Zoomed into a subfield"),
  col = c("#2166ac", "#d6604d"), lwd = 2, lty = 1:2, bty = "n"
)

# Annotations
# 1. The page's control: the exponent of the power law. This is the site's toy model, not evidence about how science changes.
# 2. Fixes the random numbers so the run is reproducible.
# 3. Five thousand scientific changes with power-law sizes.
# 4. Zoom into a subfield (the small changes) and rescale it.
# 5. The size distribution of all changes and of the zoomed subfield, on log scales. They look the same: that is what fractal means here.
