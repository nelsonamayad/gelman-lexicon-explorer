# Cheeseburger-snarfing diet gurus: evaluating teaching by ratings.
learn_effect <- 0.05 # true effect on learning (sd units) # <1>
enthusiasm <- 0.8 # novelty/enthusiasm boost to ratings
set.seed(95) # <2>

sections <- t(sapply(1:20, function(k) { # <3>
  treated <- k %% 2 == 1
  inst <- rnorm(1, 0, 0.3) # instructor effect
  pre <- rnorm(40)
  post <- 0.6 * pre + inst + treated * learn_effect + rnorm(40, 0, 0.8)
  rating <- 3.5 + inst + treated * enthusiasm * 0.5 + rnorm(40, 0, 0.6) # <4>
  c(treated = treated, gain = mean(post - 0.6 * pre), rating = mean(rating))
}))
compare <- function(v) { # <5>
  a <- v[sections[, "treated"] == 1]
  b <- v[sections[, "treated"] == 0]
  c(diff = mean(a) - mean(b), se = sqrt(var(a) / 10 + var(b) / 10))
}
rating <- compare(sections[, "rating"])
learning <- compare(sections[, "gain"])

cat(
  "Ratings up by", round(rating["diff"], 2), "points (se",
  round(rating["se"], 2), ")\n"
)
cat(
  "Effect on learning:", round(learning["diff"], 2), "sd (se",
  round(learning["se"], 2), "); true effect", learn_effect, "\n"
)

plot(sections[, "gain"], sections[, "rating"], # <6>
  pch = 19,
  col = ifelse(sections[, "treated"] == 1, "#d6604d", "#2166ac"),
  xlab = "Learning gain (section average)",
  ylab = "Student rating (section average)"
)
legend("topleft", c("New method", "Old method"),
  pch = 19,
  col = c("#d6604d", "#2166ac"), bty = "n"
)

# Annotations
# 1. The page's controls: the new method's true effect on learning, and how much novelty and enthusiasm lift the ratings.
# 2. Fixes the random numbers so the run is reproducible.
# 3. Twenty course sections, alternating between the new and the old method, each with an instructor effect, a pre-test and a post-test.
# 4. Student ratings respond to the instructor and to enthusiasm, not to what was learned.
# 5. The treated-minus-control difference and its standard error, for ratings and for learning gains.
# 6. Each section's rating against its learning gain. The new method wins on ratings and does nothing for learning.
