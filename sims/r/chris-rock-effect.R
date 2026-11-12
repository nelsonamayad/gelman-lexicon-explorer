# The Chris Rock Effect: births by day of year, averaged over weekdays.
set.seed(42) # <1>

holidays <- c( # <2>
  "1" = -0.3, "185" = -0.3, "245" = -0.3, "304" = -0.05,
  "327" = -0.3, "359" = -0.3
) # day of year: effect on log births
hol_days <- as.numeric(names(holidays))
births <- do.call(rbind, lapply(0:4, function(k) { # five years # <3>
  doy <- 1:365
  dow <- (doy - 1 + k) %% 7 # the weekday shifts each year
  hol <- ifelse(doy %in% hol_days, holidays[as.character(doy)], 0)
  near <- ifelse((doy - 1) %in% hol_days | (doy + 1) %in% hol_days, -0.06, 0)
  near[doy %in% hol_days] <- 0 # days next to a holiday dip a little
  data.frame(doy,
    weekend = dow >= 5,
    births = 10000 * exp(ifelse(dow >= 5, -0.22, 0) +
      0.05 * sin(2 * pi * (doy - 101) / 365) +
      hol + near + rnorm(365, 0, 0.025))
  )
}))
avg <- tapply( # <4>
  births$births[!births$weekend], births$doy[!births$weekend],
  mean
)

par(mfrow = c(2, 1), mar = c(4, 4, 2, 1))
plot(births$births, # <5>
  type = "l", col = "grey50", main = "Raw daily series",
  xlab = "Day (five years)", ylab = "Births"
)
plot(as.numeric(names(avg)), avg, # <6>
  type = "l", col = "#2166ac",
  main = "Day of year, averaged over weekdays", xlab = "Day of year",
  ylab = "Births"
)
abline(v = hol_days, col = "#d6604d", lty = 3)
cat(
  "Lowest weekday averages fall on days:",
  head(names(sort(avg)), 6), "\n"
)

# Annotations
# 1. Fixes the random numbers so the run is reproducible. This script has no page control: the page's only control picks which panel to show.
# 2. Six holidays and how much they lower births, on the log scale.
# 3. Five years of made-up daily births with a weekend dip, a seasonal wave, the holiday dips and noise.
# 4. The display that produces the shock of recognition: each day of the year, averaged over weekdays only.
# 5. The raw series, a blur of weekly zigzags.
# 6. The averaged series. The holiday dips and the seasonal wave are things everyone knows, now visible at once.
