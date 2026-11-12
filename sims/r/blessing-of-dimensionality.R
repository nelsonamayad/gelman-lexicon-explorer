# The Blessing of Dimensionality: more predictors, with regularization.
signal <- 0.15 # size of each true coefficient # <1>
lambda <- 40 # ridge penalty
set.seed(20) # <2>

P <- 90
n <- 100
beta <- signal * sample(c(-1, 1), P, replace = TRUE) # <3>
make <- function(m) {
  X <- matrix(rnorm(m * P), m, P)
  list(X = X, y = as.vector(X %*% beta + rnorm(m)))
}
train <- make(n)
test <- make(500)

# Ridge regression with an unpenalized intercept (lambda = 0: least squares)
ridge <- function(X, y, lambda) { # <4>
  Xc <- scale(X, scale = FALSE)
  b <- solve(
    crossprod(Xc) + (lambda + 1e-9) * diag(ncol(X)),
    crossprod(Xc, y - mean(y))
  )
  list(a = mean(y) - sum(colMeans(X) * b), b = b)
}
r2 <- function(fit, p) { # <5>
  pred <- fit$a + test$X[, 1:p, drop = FALSE] %*% fit$b
  max(-0.5, 1 - sum((test$y - pred)^2) / sum((test$y - mean(test$y))^2))
}
ps <- seq(10, 90, by = 10)
res <- t(sapply(c(5, ps), function(p) { # <6>
  X <- train$X[, 1:p, drop = FALSE]
  c(
    p = p, least_squares = r2(ridge(X, train$y, 0), p),
    ridge = r2(ridge(X, train$y, lambda), p)
  )
}))
print(round(res, 2)) # out-of-sample R squared (floored at -0.5)

matplot(res[, "p"], res[, -1], # <7>
  type = "b", pch = 19, lty = 1,
  col = c("#d6604d", "#2166ac"), xlab = "Number of predictors",
  ylab = "Out-of-sample R squared"
)
legend("bottomleft", c("Least squares", "Ridge (regularized)"),
  col = c("#d6604d", "#2166ac"), pch = 19, bty = "n"
)

# Annotations
# 1. The page's controls: the size of each true coefficient and the ridge penalty.
# 2. Fixes the random numbers so the run is reproducible.
# 3. Ninety predictors, each with a small real effect. More predictors carry more signal, if the model can use it.
# 4. Ridge regression, written out with an unpenalized intercept. A penalty of zero gives least squares.
# 5. Out-of-sample R squared on a separate test set, floored at -0.5 so a disastrous fit doesn't swamp the chart.
# 6. Fit both estimators with the first p predictors, for p from 5 to 90, against 100 training cases.
# 7. Least squares falls apart as p approaches n; the regularized fit keeps improving. That is the blessing.
