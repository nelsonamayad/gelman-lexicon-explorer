# Mister P: multilevel regression and poststratification for state opinion.
n_total <- 1200 # total sample size # <1>
old_share <- 0.75 # share of the sample that is old
set.seed(7) # <2>

S <- 50
age_gap <- 0.15 # young support 15 points higher than old
base <- 0.45 + rnorm(S, 0, 0.08) # old-person support in each state
young_share <- runif(S, 0.3, 0.6) # census share young
size <- rlnorm(S, 0, 0.8) # relative population
truth <- young_share * (base + age_gap) + (1 - young_share) * base # <3>

# Respondents: state proportional to size, age skewed old
state <- sample(S, n_total, replace = TRUE, prob = size)
young <- as.numeric(runif(n_total) > old_share) # <4>
y <- rbinom(n_total, 1, base[state] + age_gap * young)

# Step 1: common age effect, then partially pooled state intercepts
age_eff <- mean(y[young == 1]) - mean(y[young == 0]) # <5>
n <- tabulate(state, S)
raw <- tapply(y, factor(state, levels = 1:S), mean)
resid <- tapply(y - age_eff * young, factor(state, levels = 1:S), mean)
ok <- n > 0
mu <- sum(resid[ok] * n[ok]) / sum(n[ok])
v <- 0.25
tau2 <- max(0.0005, mean((resid[ok] - mu)^2) - mean(v / n[ok]))
w <- ifelse(ok, tau2 / (tau2 + v / n), 0)
old <- mu + w * (ifelse(ok, resid, mu) - mu) # <6>
# Step 2: poststratify with census age shares
mrp <- young_share * (old + age_eff) + (1 - young_share) * old # <7>

rmse <- function(est) sqrt(mean((est - truth)^2, na.rm = TRUE))
cat("Error (RMSE, percentage points): raw state means ",
  round(100 * rmse(raw), 1), ", MRP ", round(100 * rmse(mrp), 1),
  "\nStates with no respondents: ", sum(!ok), "\n",
  sep = ""
)

plot(truth, raw, # <8>
  pch = 1, col = "grey50", cex = 0.5 + sqrt(n) / 4,
  xlim = c(0.2, 0.9), ylim = c(0, 1), xlab = "True state support",
  ylab = "Estimate"
)
points(truth, mrp, pch = 19, col = "#2166ac")
abline(0, 1, lty = 2)
legend("topleft", c("Raw state mean", "MRP"),
  pch = c(1, 19),
  col = c("grey50", "#2166ac"), bty = "n"
)

# Annotations
# 1. The page's controls: the total sample size and the share of the sample that is old.
# 2. Fixes the random numbers so the run is reproducible.
# 3. Each state's true support: its young and old residents, weighted by the census share of each.
# 4. The survey over-samples the old, and small states get few respondents.
# 5. Step 1a: a common age effect, estimated from everyone.
# 6. Step 1b: each state's intercept, partially pooled toward the national mean. States with few respondents are pulled hardest.
# 7. Step 2: poststratify, weighting each state's young and old predictions by its census shares.
# 8. Raw state means (open circles, sized by sample) and MRP estimates against the truth. The small circles scatter widely; the pooled estimates don't.
