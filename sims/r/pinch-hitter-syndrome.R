# The Pinch-Hitter Syndrome: part-time players look worse than they are.
starter_share <- 0.6 # share of players who start # <1>
cold_penalty <- 0.015 # cold-start penalty on the batting average
set.seed(8) # <2>

talent <- sort(pmin(0.36, pmax(0.17, rnorm(400, 0.26, 0.025))),
  decreasing = TRUE
)
starter <- seq_along(talent) <= round(starter_share * 400) # best start # <3>
at_bats <- ifelse(starter, 500, 60)
p <- ifelse(starter, talent, talent - cold_penalty) # <4>
avg <- rbinom(400, at_bats, p) / at_bats # <5>

res <- rbind(
  Starters = c(
    talent = mean(talent[starter]),
    average = mean(avg[starter])
  ),
  "Pinch hitters" = c(
    mean(talent[!starter]),
    mean(avg[!starter])
  )
)
print(round(res, 3)) # true talent vs observed batting average

plot(talent, avg, # <6>
  pch = 19, cex = 0.6,
  col = ifelse(starter, "#2166ac", "#d6604d"),
  xlab = "True talent", ylab = "Observed batting average"
)
abline(0, 1, lty = 2)
legend("topleft", c("Starter", "Pinch hitter"),
  pch = 19,
  col = c("#2166ac", "#d6604d"), bty = "n"
)

# Annotations
# 1. The page's controls: the share of players who start, and the penalty for coming in cold.
# 2. Fixes the random numbers so the run is reproducible.
# 3. Selection: the best players start. Pinch hitters come from the rest.
# 4. The cold-start penalty: a pinch hitter performs a little below his talent.
# 5. Observed batting averages, from many at-bats for starters and few for pinch hitters.
# 6. Observed average against true talent. Pinch hitters look worse than they are for two reasons, and selection is the larger one.
