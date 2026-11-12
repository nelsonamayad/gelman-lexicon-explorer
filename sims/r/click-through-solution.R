# The Click-Through Solution: three layers for three audiences.
layer <- 2 # 1: grab attention, 2: compare, 3: check the numbers # <1>
set.seed(125) # <2>

cities <- data.frame( # <3>
  name = c(
    "Avalon", "Brookfield", "Cedar Falls", "Dunmore", "Eastport",
    "Fairview", "Glenwood", "Harbor City", "Ironton", "Juniper",
    "Kingsley", "Lakeside"
  ),
  y2015 = runif(12, 20, 80),
  region = sample(c("North", "South", "Coast"), 12, replace = TRUE)
)
cities$y2025 <- cities$y2015 + rnorm(12, 5, 8)
cols <- c(North = "#2166ac", South = "#d6604d", Coast = "#4daf4a")

if (layer == 1) { # bubbles: eye-catching, hard to compare # <4>
  plot(runif(12), runif(12),
    cex = sqrt(cities$y2025) / 1.5, pch = 19,
    col = adjustcolor(cols[cities$region], 0.6), axes = FALSE,
    xlab = "", ylab = ""
  )
} else if (layer == 2) { # positions on a common scale: easy to compare # <5>
  o <- order(cities$y2025)
  dotchart(cities$y2025[o],
    labels = cities$name[o], pch = 19,
    col = cols[cities$region[o]], xlim = range(cities[, c(2, 4)]),
    xlab = "Value (2015 open circles, 2025 dots)"
  )
  points(cities$y2015[o], seq_along(o), pch = 1)
} else { # the numbers, for checking and reuse # <6>
  print(transform(cities,
    change = round(y2025 - y2015, 1),
    y2015 = round(y2015, 1), y2025 = round(y2025, 1)
  ))
}

# Annotations
# 1. The page's control: which of the three layers to show.
# 2. Fixes the random numbers so the run is reproducible.
# 3. Twelve made-up cities with a value in 2015 and in 2025.
# 4. Layer 1, for grabbing attention: bubbles, eye-catching and hard to compare.
# 5. Layer 2, for comparing: positions on a common scale, with the earlier value as an open circle.
# 6. Layer 3, for checking and reuse: the numbers themselves.
