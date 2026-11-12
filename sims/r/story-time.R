# Story Time: a subgroup "finding" when every true effect is zero.
n_per <- 60 # people per arm per subgroup # <1>
set.seed(29) # <2>

subgroups <- c(
  "Young men", "Young women", "Older men", "Older women",
  "Urban", "Rural", "Low income", "High income", "College",
  "No college"
)
res <- t(sapply(subgroups, function(g) {
  tt <- t.test(rnorm(n_per), rnorm(n_per)) # no effect anywhere # <3>
  c(est = unname(diff(rev(tt$estimate))), p = tt$p.value)
}))
res <- res[order(-res[, "est"]), ] # <4>
print(round(res, 3))
phrase <- c(
  Urban = "urban residents", Rural = "rural residents",
  "Low income" = "people with low incomes",
  "High income" = "people with high incomes",
  College = "college graduates",
  "No college" = "people without a college degree"
)
top <- rownames(res)[1] # <5>
who <- if (top %in% names(phrase)) phrase[[top]] else tolower(top)
cat("Tonight's story: \"The program was especially effective for ", who,
  "\" (p = ", round(res[1, "p"], 3), ")\n",
  sep = ""
)

par(mar = c(4, 7, 1, 1))
plot(res[, "est"], 10:1, # <6>
  pch = 19, yaxt = "n", ylab = "",
  col = ifelse(res[, "p"] < 0.05, "#d6604d", "grey40"),
  xlab = "Estimated effect (true effect: 0)"
)
axis(2, 10:1, rownames(res), las = 1, cex.axis = 0.8)
abline(v = 0, lty = 2)

# Annotations
# 1. The page's control: people per arm in each subgroup.
# 2. Fixes the random numbers so the run is reproducible.
# 3. Ten subgroup comparisons in which the true effect is zero everywhere.
# 4. Sort them: some subgroup always comes out on top.
# 5. Tonight's protagonist, chosen by noise, with a ready-made story. A different seed picks a different hero.
# 6. The ten estimates, significant ones in red. Story time begins where the data stop.
