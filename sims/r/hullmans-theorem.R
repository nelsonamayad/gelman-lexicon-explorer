# Hullman's Theorem: experiments measure a proxy, not what we care about.
rho <- 0.5 # correlation of the proxy with the intended construct # <1>
noise <- 0.3 # experimental noise
set.seed(94) # <2>

charts <- c(
  "Bar", "Dot", "Line", "Pie", "Heatmap", "Stacked bar", "Area",
  "Slope"
)
target <- rnorm(8) # what we care about
proxy <- rho * target + sqrt(1 - rho^2) * rnorm(8) # what is measured # <3>
measured <- proxy + rnorm(8, 0, noise) # <4>

rank_measured <- rank(-measured) # <5>
rank_target <- rank(-target)
cat(
  "Rank correlation between the experiment's ranking and the ranking",
  "on the intended construct:", round(cor(rank_measured, rank_target), 2),
  "\n"
)

plot(c(1, 2), c(1, 8),
  type = "n", xlim = c(0.5, 2.5), ylim = c(8.5, 0.5),
  xaxt = "n", xlab = "", ylab = "Rank"
)
axis(1, 1:2, c("Experiment", "Intended construct"))
segments(1, rank_measured, 2, rank_target, # <6>
  col = ifelse(abs(rank_measured - rank_target) > 2, "#d6604d",
    "grey60"
  ), lwd = 2
)
text(0.95, rank_measured, charts, adj = 1, cex = 0.8)

# Annotations
# 1. The page's controls: how well the measured proxy correlates with what we care about, and how noisy the experiment is.
# 2. Fixes the random numbers so the run is reproducible.
# 3. What the experiment can measure, which is only correlated with what we care about.
# 4. What the experiment actually records, with its own noise.
# 5. The experiment's ranking of the eight chart types.
# 6. Lines connect each chart type's experimental rank to its rank on the intended construct. Red lines move by more than two places.
