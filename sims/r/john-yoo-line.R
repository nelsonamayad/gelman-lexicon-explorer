# The John Yoo Line: once trust is lost, careful work goes unnoticed.
lapse_start <- 15 # when the author gets careless (piece #) # <1>
lapse_length <- 12 # how long the lapse lasts
line <- 0.5 # trust threshold (the line)
set.seed(41) # <2>

# Belief that the author is reliable (right 90% of the time) rather than a
# hack (30%). Below the line, readers mostly stop paying attention.
log_odds <- 3
trust <- numeric(60)
for (t in 1:60) {
  careless <- t > lapse_start & t <= lapse_start + lapse_length
  good <- runif(1) < if (careless) 0.3 else 0.9 # <3>
  noticed <- plogis(log_odds) >= line || runif(1) < 0.15 # <4>
  if (noticed) {
    log_odds <- log_odds + if (good) log(0.9 / 0.3) else log(0.1 / 0.7) # <5>
  }
  log_odds <- min(12, max(-12, log_odds))
  trust[t] <- plogis(log_odds)
}
below <- which(trust < line)
if (length(below)) {
  cat("Trust falls below the line at piece ", below[1], "\n", sep = "")
  back <- which(trust >= line & seq_along(trust) > below[1])
  cat(if (length(back)) {
    paste("Back above the line at piece", back[1])
  } else {
    "Trust never recovers within 60 pieces"
  }, "\n", sep = "")
} else {
  cat("Trust never falls below the line\n")
}

plot(1:60, trust, # <6>
  type = "l", lwd = 2, col = "#2166ac", ylim = c(0, 1),
  xlab = "Piece", ylab = "Audience trust"
)
rect(lapse_start + 0.5, -1, lapse_start + lapse_length + 0.5, 2,
  col = adjustcolor("#d6604d", 0.1), border = NA
)
abline(h = line, lty = 2)

# Annotations
# 1. The page's controls: when the author's careless stretch starts, how long it lasts, and where the trust threshold sits.
# 2. Fixes the random numbers so the run is reproducible.
# 3. Each piece is good with high probability, except during the careless stretch.
# 4. Readers notice a piece only while they still trust the author, or by chance.
# 5. A noticed piece updates the readers' belief that the author is reliable.
# 6. Trust over 60 pieces. Once it falls below the line, careful work goes unread and trust rarely recovers.
