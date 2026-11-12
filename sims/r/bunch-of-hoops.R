# A bunch of hoops: checks that false findings pass easily.
pi_true <- 0.4 # share of findings that are true # <1>
gaming <- 0.85 # how easily false findings pass each hoop
set.seed(93) # <2>

real <- runif(2000) < pi_true
pass <- function(p_true, p_false) runif(2000) < ifelse(real, p_true, p_false)
hoops <- pass(0.95, gaming) & pass(0.95, gaming) & pass(0.95, gaming) # <3>
substantive <- pass(0.8, 0.15) # e.g. a replication # <4>

ppv <- function(passed) mean(real[passed]) # <5>
cat("True among findings that pass the hoops: ",
  round(100 * ppv(hoops)), "% (base rate ", 100 * pi_true, "%)\n",
  sep = ""
)
cat("True among findings that pass the substantive check: ",
  round(100 * ppv(substantive)), "%\n",
  sep = ""
)

rates <- rbind(
  Hoops = c(mean(hoops[real]), mean(hoops[!real])),
  Substantive = c(
    mean(substantive[real]),
    mean(substantive[!real])
  )
)
barplot(t(rates), # <6>
  beside = TRUE, col = c("#2166ac", "#d6604d"),
  ylim = c(0, 1), ylab = "Share that pass"
)
legend("topright", c("True findings", "False findings"),
  fill = c("#2166ac", "#d6604d"), bty = "n"
)

# Annotations
# 1. The page's controls: the share of findings that are true, and how easily a false finding passes a hoop.
# 2. Fixes the random numbers so the run is reproducible.
# 3. Three hoops in a row. True findings pass each one 95% of the time; false ones pass almost as often, so the hoops barely discriminate.
# 4. One substantive check, such as a replication, that false findings mostly fail.
# 5. The share of true findings among those that pass: what a reader learns from seeing the check passed.
# 6. Pass rates for true and false findings under each kind of check.
