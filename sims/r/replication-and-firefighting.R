# Replication and firefighting: suppressing small fires feeds a big one.
suppression <- 0.85 # suppression of routine criticism # <1>
set.seed(139) # <2>

crisis_year <- sample(30:55, 1) # when the crisis comes # <3>
run <- function(sup) {
  fuel <- 10
  path <- numeric(61)
  burned <- 0
  for (t in 0:60) {
    if (t == crisis_year) {
      burned <- fuel
      fuel <- 0
    }
    path[t + 1] <- fuel
    fuel <- fuel + 20 - fuel * 0.25 * (1 - sup) # criticism burns 25%/yr # <4>
  }
  list(path = path, burned = burned)
}
yours <- run(suppression)
open <- run(0)
cat("Crisis in year ", crisis_year, ": it burns ", round(yours$burned),
  " units of unexamined work with your suppression level, ",
  round(open$burned), " with none\n",
  sep = ""
)

matplot(0:60, cbind(yours$path, open$path), # <5>
  type = "l", lty = 1, lwd = 2,
  col = c("#d6604d", "#2166ac"), xlab = "Year",
  ylab = "Unexamined work (fuel)"
)
abline(v = crisis_year, lty = 2)
legend("topleft", c(
  "Your suppression level",
  "No suppression (controlled burns)"
),
col = c("#d6604d", "#2166ac"), lwd = 2, bty = "n"
)

# Annotations
# 1. The page's control: how much routine criticism is suppressed.
# 2. Fixes the random numbers so the run is reproducible.
# 3. A replication crisis arrives at some point and burns all the unexamined work at once.
# 4. Each year new work arrives and routine criticism burns off a share of the backlog, unless it is suppressed.
# 5. Unexamined work over time. Suppressing the small fires lets the fuel build up for the big one.
