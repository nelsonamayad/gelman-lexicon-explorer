# The Garden of Forking Paths: one test, chosen by looking at the data.
n <- 100 # participants per arm # <1>
set.seed(44) # <2>

p_value <- function(a, b) { # two-sample test (normal approximation)
  z <- (mean(a) - mean(b)) / sqrt(var(a) / length(a) + var(b) / length(b))
  2 * pnorm(-abs(z))
}
trim <- function(a) a[abs(a - mean(a)) < 2.5 * sd(a)]
diff <- function(a, b) abs(mean(a) - mean(b))
make <- function() { # heavy-ish tails, so outliers occur; no true effect # <3>
  y1 <- rt(n, 5)
  data.frame(y1,
    y2 = 0.5 * y1 + sqrt(0.75) * rt(n, 5),
    sex = rbinom(n, 1, 0.5)
  )
}
pick <- function(D, grp, out) D[[out]][grp == "all" | D$sex == grp]

res <- t(replicate(1000, {
  trt <- make()
  ctl <- make()
  # 1. Preregistered: always the same test
  pre <- p_value(trt$y1, ctl$y1) < 0.05 # <4>
  # 2. Forking paths: three choices made by looking at the data
  out <- if (diff(trt$y2, ctl$y2) > diff(trt$y1, ctl$y1)) "y2" else "y1" # <5>
  d0 <- diff(pick(trt, 0, out), pick(ctl, 0, out))
  d1 <- diff(pick(trt, 1, out), pick(ctl, 1, out))
  grp <- if (d1 > 2 * d0) 1 else if (d0 > 2 * d1) 0 else "all"
  a <- pick(trt, grp, out)
  b <- pick(ctl, grp, out)
  if (diff(trim(a), trim(b)) > diff(a, b)) {
    a <- trim(a)
    b <- trim(b)
  }
  forked <- p_value(a, b) < 0.05 # <6>
  # 3. Fishing: test all 12 paths and report the smallest p-value
  ps <- c() # <7>
  for (o in c("y1", "y2")) {
    for (tr in c(FALSE, TRUE)) {
      for (g in c("all", 0, 1)) {
        a <- pick(trt, g, o)
        b <- pick(ctl, g, o)
        if (tr) {
          a <- trim(a)
          b <- trim(b)
        }
        ps <- c(ps, p_value(a, b))
      }
    }
  }
  c(preregistered = pre, forking_paths = forked, fishing = min(ps) < 0.05)
}))
rates <- colMeans(res)
print(round(100 * rates, 1)) # false-positive rates (%), true effect zero

barplot(rates, # <8>
  col = c("grey60", "#d6604d", "#67001f"), ylim = c(0, 0.5),
  ylab = "False-positive rate (true effect is zero)"
)
abline(h = 0.05, lty = 2)

# Annotations
# 1. The page's control: participants per arm.
# 2. Fixes the random numbers so the run is reproducible.
# 3. One arm of one study: two outcomes, a sex variable and heavy-ish tails so outliers occur. The true effect is zero.
# 4. The preregistered researcher always runs the same test.
# 5. The forking-paths researcher looks at the data, not at p-values, and chooses the outcome with the larger difference, then a subgroup, then whether to drop outliers.
# 6. That researcher computes exactly one p-value.
# 7. The fishing researcher runs all twelve paths and reports the best.
# 8. False-positive rates. One data-chosen test lands between the nominal rate and fishing: no fishing was needed, only forks.
