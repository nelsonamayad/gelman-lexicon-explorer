# The camel that is the likelihood: the data model outweighs the prior.
n_out <- 3 # number of outliers # <1>
out_size <- 10 # outlier size
set.seed(99) # <2>

y <- c(rnorm(30, 1, 1), out_size + rnorm(n_out)) # <3>
grid <- seq(-4, 12, by = 0.02) # grid of values for the mean
post_mean <- function(prior_sd, likelihood) { # <4>
  loglik <- sapply(grid, function(m) {
    if (likelihood == "normal") {
      sum(dnorm(y, m, 1, log = TRUE))
    } else {
      sum(dt(y - m, df = 3, log = TRUE))
    }
  })
  lp <- dnorm(grid, 0, prior_sd, log = TRUE) + loglik
  w <- exp(lp - max(lp))
  sum(w * grid) / sum(w)
}
res <- sapply(c(1, 10), function(s) { # <5>
  sapply(
    c("normal", "t3"),
    function(l) post_mean(s, l)
  )
})
colnames(res) <- c("prior sd 1", "prior sd 10")
print(round(res, 3)) # posterior means
cat(
  "Changing the prior moves the estimate by",
  round(abs(res["normal", 1] - res["normal", 2]), 3), "(the gnat)\n"
)
cat(
  "Changing the likelihood moves it by",
  round(abs(res["normal", 2] - res["t3", 2]), 3), "(the camel)\n"
)

barplot(res, # <6>
  beside = TRUE, col = c("#d6604d", "#2166ac"),
  ylab = "Posterior mean",
  legend.text = c("Normal", "Student-t (3 df)")
)

# Annotations
# 1. The page's controls: how many outliers there are and how far out they sit.
# 2. Fixes the random numbers so the run is reproducible.
# 3. Thirty ordinary observations plus a few outliers.
# 4. The posterior mean of the location, computed on a grid, under a normal or a Student-t likelihood and a normal prior of the given width.
# 5. All four combinations: two priors by two likelihoods.
# 6. Changing the prior barely moves the estimate (the gnat). Changing the likelihood moves it a lot (the camel).
