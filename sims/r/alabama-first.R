# Alabama First: the same 50 states sorted three ways.
order_by <- "alphabetical" # "alphabetical", "value" or "region" # <1>
region_gap <- 6 # size of regional differences
set.seed(14) # <2>

region <- as.character(state.region) # R's built-in census regions
region[region == "North Central"] <- "Midwest"
effect <- c(Northeast = 1, Midwest = 0, South = -1, West = 0.4)
value <- 50 + region_gap * effect[region] + rnorm(50, 0, 3) # <3>
states <- data.frame(state = state.name, region, value)

states <- switch(order_by, # <4>
  alphabetical = states,
  value = states[order(-states$value), ],
  region = states[order(states$region, -states$value), ]
)
cols <- c(
  Midwest = "#2166ac", Northeast = "#d6604d", South = "#1a9850",
  West = "#984ea3"
)
dotchart(rev(states$value), # <5>
  labels = rev(states$state), pch = 19,
  col = cols[rev(states$region)], cex = 0.6,
  xlab = "Simulated outcome"
)
legend("bottomright", names(cols), col = cols, pch = 19, cex = 0.7)
cat("Regional gap (Northeast minus South):", 2 * region_gap, "points\n")

# Annotations
# 1. The page's controls: how to order the states, and how large the regional differences are.
# 2. Fixes the random numbers so the run is reproducible.
# 3. A made-up outcome with a regional pattern plus noise. R's built-in census regions supply the structure.
# 4. The same 50 values, ordered alphabetically (Alabama first), by value, or by region and then value.
# 5. The dot chart. Alphabetical order hides the regional pattern that the other two orders make obvious.
