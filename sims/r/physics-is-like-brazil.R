# Physics is like Brazil, statistics is like Chile: how soon do you reach
# the frontier?
trek <- 8 # Brazil: years of study before reaching the frontier # <1>
p_hit <- 0.25 # Chile: chance a routine project hits an open problem
set.seed(143) # <2>

# Year each of 1000 students first works on an open problem (Inf = never)
reach <- function(first_year, p) { # <3>
  replicate(1000, {
    hit <- which(1:15 >= first_year & runif(15) < p)
    if (length(hit)) hit[1] else Inf
  })
}
physics <- reach(trek, 0.35) # <4>
statistics <- reach(1, p_hit) # <5>
share <- sapply(0:15, function(y) {
  c(
    physics = mean(physics <= y),
    statistics = mean(statistics <= y)
  )
})
cat("Reached the frontier by year 5: physics ",
  round(100 * share["physics", 6]), "%, statistics ",
  round(100 * share["statistics", 6]), "%\n",
  sep = ""
)

matplot(0:15, t(share), # <6>
  type = "s", lty = 1, lwd = 2, ylim = c(0, 1),
  col = c("#d6604d", "#2166ac"), xlab = "Years of study",
  ylab = "Share who have worked on an open problem"
)
legend("topleft", c("Physics (Brazil)", "Statistics (Chile)"),
  col = c("#d6604d", "#2166ac"), lwd = 2, bty = "n"
)

# Annotations
# 1. The page's controls: how many years of study physics demands before the frontier, and how likely a routine statistics project is to hit an open problem.
# 2. Fixes the random numbers so the run is reproducible.
# 3. The year each of 1,000 students first works on an open problem, given when they are allowed to start and how likely each year is to succeed.
# 4. Physics is like Brazil: a long trek inland before the mountains.
# 5. Statistics is like Chile: the mountains are a few steps from the beach.
# 6. The share of students who have reached the frontier, year by year.
