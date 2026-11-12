# The Backseat Driver Principle: listen to criticism, even rude criticism.
precision <- 0.25 # share of critiques that are correct # <1>
rude_correct <- 0.6 # probability that a correct critique is rude
set.seed(10) # <2>

run <- function(listen_to_all) { # <3>
  errors <- 12
  path <- errors
  for (t in 1:40) { # one critique per round
    correct <- errors > 0 && runif(1) < precision # <4>
    rude <- if (correct) runif(1) < rude_correct else runif(1) < 0.5
    if (correct && (listen_to_all || !rude)) errors <- errors - 1 # <5>
    path <- c(path, errors)
  }
  path
}
everyone <- run(TRUE)
polite_only <- run(FALSE)

cat(
  "Errors left after 40 rounds: listens to everyone", tail(everyone, 1),
  "| ignores rude critics", tail(polite_only, 1), "\n"
)

matplot(0:40, cbind(everyone, polite_only), # <6>
  type = "s", lty = 1, lwd = 2,
  col = c("#2166ac", "#d6604d"), xlab = "Round",
  ylab = "Errors left (of 12)"
)
legend("topright", c("Listen to everyone", "Ignore rude critics"),
  col = c("#2166ac", "#d6604d"), lwd = 2, bty = "n"
)

# Annotations
# 1. The page's controls: the share of critiques that are correct, and how often a correct critique is rude.
# 2. Fixes the random numbers so the run is reproducible.
# 3. A researcher with 12 errors receives one critique per round for 40 rounds. The argument says whether rude critiques get a hearing.
# 4. Each critique is correct with the given probability, as long as there are errors left to find.
# 5. A correct critique fixes an error only if the researcher listens to it. Ignoring rude critics throws away the correct ones among them.
# 6. Errors left over time under the two policies.
