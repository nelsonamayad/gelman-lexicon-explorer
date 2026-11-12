# Clarke's Law: the GRIM test can't tell crappy research from fraud.
error_rate <- 0.4 # sloppiness: probability a reported mean has an error # <1>
set.seed(59) # <2>

r2 <- function(x) round(x, 2)
grim_ok <- function(m, n) { # can n integers have mean m (to 2 decimals)? # <3>
  k <- round(m * n)
  any(sprintf("%.2f", r2((k - 1):(k + 1) / n)) == sprintf("%.2f", m))
}
report <- function(type) { # <4>
  replicate(2000, {
    n <- sample(10:40, 1)
    m <- r2(mean(sample(1:7, n, replace = TRUE))) # a 1-7 rating scale
    if (type == "Sloppy" && runif(1) < error_rate) {
      m <- r2(m + sample(c(-1, 1), 1) * sample(1:9, 1) / 100)
    }
    if (type == "Fabricated") m <- r2(runif(1, 2, 6))
    grim_ok(m, n)
  })
}
fail <- sapply( # <5>
  c("Honest", "Sloppy", "Fabricated"),
  function(type) 1 - mean(report(type))
)
print(round(100 * fail)) # GRIM failure rates (%)

barplot(fail, # <6>
  col = c("#2166ac", "#e6ab02", "#d6604d"), ylim = c(0, 1),
  ylab = "Share of means that fail the GRIM test"
)

# Annotations
# 1. The page's control: how often a sloppy researcher's reported mean contains an error.
# 2. Fixes the random numbers so the run is reproducible.
# 3. The GRIM test: with n integer responses, can any integer total divided by n give the reported mean to two decimals?
# 4. Two thousand reported means from honest, sloppy or fabricated research. Sloppy means get a small transcription error; fabricated ones are made up.
# 5. The share of each kind that fails the test.
# 6. Honest means never fail. Sloppy and fabricated ones both do, and the test cannot tell the two apart: sufficiently crappy research is indistinguishable from fraud.
