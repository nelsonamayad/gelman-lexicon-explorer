# The Horse: keep beating it, or the refuted finding keeps spreading.
q_beat <- 0.5 # share of new citers who learn of the refutation # <1>
q_stop <- 0.1 # the same share if critics stop
growth <- 1.15 # citation growth factor
# Deterministic: no random numbers.

years <- 0:25
keep <- 100 * (growth * (1 - q_beat))^years # uncritical citations/year # <2>
stop <- 100 * (growth * (1 - q_stop))^years # <3>
cat("After 25 years, uncritical citations per year: ",
  round(tail(keep, 1), 1), " if critics keep at it, ",
  round(tail(stop, 1), 1), " if they stop\n",
  sep = ""
)

matplot(years, cbind(keep, stop), # <4>
  type = "l", lty = 1, lwd = 2, log = "y",
  col = c("#2166ac", "#d6604d"), xlab = "Year",
  ylab = "Uncritical citations per year"
)
legend("left", c(
  "Critics keep beating the horse",
  "Critics stop: 'everyone knows'"
),
col = c("#2166ac", "#d6604d"), lwd = 2, bty = "n"
)

# Annotations
# 1. The page's controls: the share of new citers who learn of the refutation while critics keep at it, the same share once they stop, and how fast citations grow. There is no seed: the model is deterministic.
# 2. Uncritical citations per year if the critics keep beating the horse.
# 3. The same if they stop because everyone knows.
# 4. Both paths on a log scale. The audience keeps changing, so the horse is never really dead.
