# Tell Me What You Don't Know: asking about uncertainty widens intervals.
k <- 0.5 # overconfidence factor (1 = calibrated) # <1>
prompt <- 0.6 # how much the question helps
set.seed(49) # <2>

k_after <- k + prompt * (1 - k) # <3>
sigma <- exp(rnorm(200, 0, 0.5)) # real uncertainty of 200 questions
truth <- rnorm(200, 0, sigma) # error of the expert's best guess
cover_before <- abs(truth) < 1.645 * k * sigma # stated 90% interval # <4>
cover_after <- abs(truth) < 1.645 * k_after * sigma # after the question
cat("Coverage of stated 90% intervals: initial ",
  round(100 * mean(cover_before)), "%, after \"tell me what you don't ",
  "know\" ", round(100 * mean(cover_after)), "%\n",
  sep = ""
)

q <- 1:50
plot(q, truth[q], pch = 19, ylim = range(truth[q], 1.645 * k_after * # <5>
  c(-1, 1) * max(sigma[q])), xlab = "Question", ylab = "Error")
segments(q, -1.645 * k_after * sigma[q], q, 1.645 * k_after * sigma[q],
  col = "#2166ac", lwd = 3
)
segments(q, -1.645 * k * sigma[q], q, 1.645 * k * sigma[q],
  col = "#d6604d", lwd = 2
)

# Annotations
# 1. The page's controls: the expert's overconfidence (1 is calibrated) and how much the question helps.
# 2. Fixes the random numbers so the run is reproducible.
# 3. After being asked what they don't know, the expert's intervals widen part of the way toward calibration.
# 4. Coverage of the expert's stated 90% intervals before the question.
# 5. The expert's errors with the intervals before (red) and after (blue) the question. The wider intervals cover more of the errors.
