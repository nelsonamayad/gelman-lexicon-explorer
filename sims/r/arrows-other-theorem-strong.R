# Arrow's Other Theorem (strong form): one result counted m times.
m <- 5 # times each result is published # <1>
K <- 6 # independent studies, all of a true effect of zero
set.seed(34) # <2>

fpr <- sapply(1:5, function(mm) {
  pooled <- rowMeans(matrix(rnorm(2000 * K), ncol = K)) # 2,000 analyses # <3>
  se <- 1 / sqrt(K * mm) # naive standard error, counting copies # <4>
  mean(2 * pnorm(-abs(pooled) / se) < 0.05)
})
cat(
  "False-positive rate with each result published", m, "times:",
  paste0(round(100 * fpr[m], 1), "%"), "\n"
)

barplot(fpr, # <5>
  names.arg = 1:5, ylim = c(0, 0.6),
  col = ifelse(1:5 == m, "#d6604d", "grey70"),
  xlab = "Publications per result (m)",
  ylab = "False-positive rate of the meta-analysis"
)
abline(h = 0.05, lty = 2)

# Annotations
# 1. The page's controls: how many times each result is published, and how many independent studies there really are.
# 2. Fixes the random numbers so the run is reproducible.
# 3. Two thousand meta-analyses, each pooling K independent studies of a true effect of zero.
# 4. A naive meta-analysis counts every copy as a new study, so its standard error shrinks as if there were K times m studies.
# 5. The false-positive rate at each number of copies. The dashed line is the nominal 5%.
