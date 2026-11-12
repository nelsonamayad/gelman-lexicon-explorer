# The worst visual display of all time: the Stroop test in black and white.
bw <- FALSE # print in black and white? # <1>
set.seed(109) # <2>

# Reaction times (ms). Ink that conflicts with the word slows reading,
# but only if the reader can see the colors.
trial <- function(incongruent) {
  base <- rlnorm(400, log(600), 0.15)
  base + if (incongruent && !bw) rnorm(400, 120, 40) else 0 # <3>
}
congruent <- trial(FALSE)
incongruent <- trial(TRUE)
cat("Interference effect (incongruent minus congruent): ",
  round(mean(incongruent) - mean(congruent)), " ms\n",
  sep = ""
)

boxplot(list(Congruent = congruent, Incongruent = incongruent), # <4>
  col = c("grey70", if (bw) "grey70" else "#d6604d"),
  ylab = "Reaction time (ms)"
)

# Annotations
# 1. The page's control: whether the test is printed in black and white.
# 2. Fixes the random numbers so the run is reproducible.
# 3. The Stroop interference: conflicting ink slows the reader, but only if the reader can see the colors.
# 4. Reaction times for congruent and incongruent words. In black and white the effect vanishes, and the display can't do its one job.
