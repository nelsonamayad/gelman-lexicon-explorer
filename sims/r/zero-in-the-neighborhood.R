# If zero is in the neighborhood, invite it in.
level <- 5 # typical level of the series # <1>
set.seed(100) # <2>

v <- level + cumsum(rnorm(24, 0.15, 0.6)) # a series over 24 periods # <3>
lo <- min(v)
hi <- max(v)
invite <- lo <= 0 || lo < 1.5 * (hi - lo) # is zero in the neighborhood? # <4>
cat("The data range from ", round(lo, 1), " to ", round(hi, 1), ": ",
  if (invite) {
    "zero is in the neighborhood, so include it"
  } else {
    "zero is far away, so keep the zoomed axis"
  }, "\n",
  sep = ""
)

par(mfrow = c(1, 2)) # <5>
plot(1:24, v,
  type = "b", pch = 19, main = "Zoomed axis", xlab = "Period",
  ylab = "Value"
)
plot(1:24, v,
  type = "b", pch = 19, ylim = c(min(0, lo), hi),
  main = "Axis including zero", xlab = "Period", ylab = "Value"
)

# Annotations
# 1. The page's control: the typical level of the series.
# 2. Fixes the random numbers so the run is reproducible.
# 3. A series over 24 periods.
# 4. The site's rule of thumb: invite zero in when its distance from the data is comparable to the data's own spread.
# 5. The same series on the software's zoomed axis and on an axis that includes zero.
