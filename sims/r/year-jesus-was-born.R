# The year Jesus was born: center your predictors.
center <- 0 # 0 (no centering), 1950, or "mean" # <1>
# Deterministic: no random numbers. Men's world records in the mile,
# 1913-1999, in seconds.
mile <- data.frame( # <2>
  year = c(
    1913, 1915, 1923, 1931, 1933, 1934, 1937, 1942, 1942, 1942,
    1943, 1944, 1945, 1954, 1954, 1957, 1958, 1962, 1964, 1965,
    1966, 1967, 1975, 1975, 1979, 1980, 1981, 1981, 1981, 1985,
    1993, 1999
  ),
  time = c(
    254.4, 252.6, 250.4, 249.2, 247.6, 246.8, 246.4, 246.2, 246.2,
    244.6, 242.6, 241.6, 241.4, 239.4, 238.0, 237.2, 234.5, 234.4,
    234.1, 233.6, 231.3, 231.1, 231.0, 229.4, 229.0, 228.8, 228.53,
    228.40, 227.33, 226.32, 224.39, 223.13
  )
)
c0 <- if (center == "mean") mean(mile$year) else center
fit <- lm(time ~ I(year - c0), data = mile) # <3>
print(round(summary(fit)$coefficients[, 1:2], 3))
cat("The intercept is the record time in the year ", round(c0), "\n",
  sep = ""
)

plot(mile$year, mile$time, # <4>
  pch = 19, xlab = "Year",
  ylab = "World record, mile (seconds)"
)
abline(
  a = coef(fit)[1] - coef(fit)[2] * c0, b = coef(fit)[2],
  col = "#2166ac", lwd = 2
)

# Annotations
# 1. The page's control: where to center the year, at 0, at 1950 or at the mean. There is no seed: the data are real.
# 2. Men's world records in the mile, 1913 to 1999.
# 3. The regression on the centered year. Uncentered, the intercept is the predicted record in the year Jesus was born, a number nobody wants.
# 4. The records with the fitted line.
