# McBroom's Law: sources that never correct their errors lose credibility.
n_errors <- 4 # number of falsehoods exposed # <1>
p_fix_reliable <- 0.8 # chance a reliable source corrects an error
p_fix_unreliable <- 0.3 # chance an unreliable source corrects an error
# Deterministic: no random numbers. A reader starts 80% sure the source is
# reliable; an exposed error is 3 times likelier from an unreliable source.

lr_error <- log(0.1 / 0.3) # <2>
lr_fix <- log(p_fix_reliable / p_fix_unreliable) # <3>
lr_no_fix <- log((1 - p_fix_reliable) / (1 - p_fix_unreliable))
k <- 0:n_errors
corrects <- plogis(log(0.8 / 0.2) + k * (lr_error + lr_fix)) # <4>
never <- plogis(log(0.8 / 0.2) + k * (lr_error + lr_no_fix)) # <5>

cat("Belief the source is reliable after ", n_errors, " exposed errors: ",
  "corrects ", round(100 * tail(corrects, 1)), "% | never corrects ",
  round(100 * tail(never, 1)), "%\n",
  sep = ""
)

matplot(k, cbind(corrects, never), # <6>
  type = "b", pch = 19, lty = 1,
  col = c("#2166ac", "#d6604d"), ylim = c(0, 1),
  xlab = "Falsehoods exposed", ylab = "Belief the source is reliable"
)
legend("bottomleft", c("Takes accountability", "Never takes accountability"),
  col = c("#2166ac", "#d6604d"), pch = 19, bty = "n"
)

# Annotations
# 1. The page's controls: how many falsehoods are exposed, and how likely a reliable and an unreliable source are to correct one. There is no seed: the model is deterministic.
# 2. Each exposed error is evidence against reliability, because unreliable sources make more of them.
# 3. A correction is evidence for reliability, because reliable sources correct more often.
# 4. The reader's belief after each error for a source that corrects.
# 5. The same for a source that never corrects: the same errors, plus the extra evidence of silence.
# 6. Belief in the source's reliability as the errors mount. The refusal to correct is the more informative part.
