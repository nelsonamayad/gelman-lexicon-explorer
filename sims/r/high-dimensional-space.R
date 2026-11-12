# In high-dimensional space, no one can hear you scream.
d <- 100 # dimension # <1>
set.seed(132) # <2>

dist <- sqrt(rowSums(matrix(rnorm(5000 * d), ncol = d)^2)) # from the mode # <3>

cat("Distance from the mode: ", round(mean(dist), 2), " +/- ",
  round(sd(dist), 2), " (sqrt(d) = ", round(sqrt(d), 2), ")\n",
  sep = ""
)
cat("Share of draws within distance 1 of the mode: ",
  round(100 * mean(dist < 1), 2), "%\n",
  sep = ""
)

hist(dist, # <4>
  breaks = 40, col = "#2166ac", border = "white", main = "",
  xlim = c(0, max(dist)), xlab = "Distance from the mode",
  ylab = "Draws"
)
abline(v = 0, col = "#d6604d", lwd = 3)

# Annotations
# 1. The page's control: the number of dimensions.
# 2. Fixes the random numbers so the run is reproducible.
# 3. The distance from the mode of 5,000 draws from a standard normal in d dimensions. It concentrates near the square root of d.
# 4. The histogram of distances. The mode, in red at zero, is where the density is highest and where no draw ever goes.
