# Deference Trap: errors spread through a literature that never checks itself.
base_error <- 0.1 # chance a new study is wrong on its own # <1>
inherit <- 0.4 # chance a wrong foundation compromises a study
check_rate <- 0.2 # share of wrong studies caught by meta-science each round
set.seed(87) # <2>

run <- function(check) { # <3>
  wrong <- runif(100) < base_error
  flagged <- rep(FALSE, 100)
  share <- mean(wrong)
  for (g in 1:15) { # 15 generations of 100 studies
    flagged <- flagged | (wrong & runif(length(wrong)) < check) # <4>
    usable <- which(!flagged)
    if (length(usable) == 0) usable <- seq_along(wrong)
    new <- runif(100) < base_error
    for (k in 1:3) { # each new study builds on three earlier ones
      cited <- usable[sample.int(length(usable), 100, replace = TRUE)]
      new <- new | (wrong[cited] & runif(100) < inherit) # <5>
    }
    keep <- max(1, length(wrong) - 199):length(wrong) # the last 200
    wrong <- c(wrong[keep], new)
    flagged <- c(flagged[keep], rep(FALSE, 100))
    share <- c(share, mean(new))
  }
  share
}
deference <- run(0)
checked <- run(check_rate)

cat("Compromised after 15 generations: ", round(100 * tail(deference, 1)),
  "% with pure deference, ", round(100 * tail(checked, 1)),
  "% with meta-science checking\n",
  sep = ""
)

matplot(0:15, cbind(deference, checked), # <6>
  type = "l", lty = 1, lwd = 2,
  col = c("#d6604d", "#2166ac"), ylim = c(0, 1), xlab = "Generation",
  ylab = "Share of new studies compromised"
)
legend("topleft", c("No meta-science", "With meta-science checking"),
  col = c("#d6604d", "#2166ac"), lwd = 2, bty = "n"
)

# Annotations
# 1. The page's controls: how often a new study is wrong on its own, how often a wrong foundation compromises a study that builds on it, and how much of the wrong work meta-science catches each round.
# 2. Fixes the random numbers so the run is reproducible.
# 3. Fifteen generations of 100 studies, with or without meta-science checking.
# 4. Checking: some of the wrong studies get flagged and are no longer built on.
# 5. Deference: each new study builds on three earlier ones and inherits their errors.
# 6. The share of new studies compromised, generation by generation.
