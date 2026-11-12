# Context: in the coincidence frame, how often does an uncanny event happen?
readers <- 100 # readers (thousands) # <1>
one_in <- 1000 # chance a dead device revives in a year: 1 in ...
special <- 3 # days a year that carry special meaning
set.seed(111) # <2>

lambda <- readers * 1000 / one_in * special / 365 # expected per year # <3>
per_year <- rpois(50, lambda) # 50 simulated years # <4>

cat("Expected coincidences per year:", round(lambda, 1), "\n")
cat("Years (of 50) with at least one:", sum(per_year > 0), "\n")

plot(1975:2024, per_year, # <5>
  type = "h", lwd = 4, col = "#2166ac",
  xlab = "Year", ylab = "Readers with an uncanny revival"
)

# Annotations
# 1. The page's controls: how many readers there are, how rare the event is, and how many days a year would count as uncanny.
# 2. Fixes the random numbers so the run is reproducible.
# 3. The expected number of uncanny coincidences per year, once the whole context is counted: many readers, many devices, several meaningful days.
# 4. Fifty simulated years of coincidences.
# 5. Coincidences per year. In the right frame, the uncanny is routine.
