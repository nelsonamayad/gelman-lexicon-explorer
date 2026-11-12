# Theoretical and applied statisticians: model y given x, then transfer.
skew <- 1 # how over-sampled high-x units are # <1>
slope <- 1 # slope of y on x
set.seed(12) # <2>

target_x <- rnorm(5000, 0, 1) # the population we care about
x <- rnorm(300, skew, 1) # the sample over-represents high x # <3>
y <- 2 + slope * x + rnorm(300)
fit <- lm(y ~ x) # <4>
cat("True population mean of y: 2\n",
  "Sample mean of y: ", round(mean(y), 2), "\n",
  "Regression, averaged over the population's x: ",
  round(mean(predict(fit, data.frame(x = target_x))), 2), "\n", # <5>
  sep = ""
)

plot(x, y, # <6>
  pch = 19, cex = 0.5, col = "grey50", xlim = c(-4, 4),
  xlab = "x", ylab = "y"
)
abline(fit, col = "#2166ac", lwd = 2)
rug(target_x[1:600], col = "#d6604d")

# Annotations
# 1. The page's controls: how over-sampled high-x units are, and the slope of y on x.
# 2. Fixes the random numbers so the run is reproducible.
# 3. The sample over-represents high values of x, so its mean of y is wrong for the population.
# 4. The applied statistician's move: model y given x.
# 5. Then average the predictions over the population's x. This is poststratification in miniature.
# 6. The sample with the fitted line, and the population's x distribution as a rug along the bottom.
