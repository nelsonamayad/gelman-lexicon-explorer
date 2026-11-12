# The Taxonomy of Confusion: which questions still reach the TA?
help_scale <- 1 # how well the self-help steps work (1 = baseline) # <1>
set.seed(19) # <2>

kinds <- data.frame( # <3>
  kind = c(
    "1. Prerequisite statistics", "2. Course statistics",
    "3. Don't know the function's name",
    "4. Don't know how the function works",
    "5. Code gives an error", "6. Code runs but is wrong"
  ),
  share = c(0.15, 0.25, 0.15, 0.15, 0.18, 0.12),
  self_help = c(0.8, 0.6, 0.85, 0.75, 0.6, 0.35)
)
q <- sample(6, 300, replace = TRUE, prob = kinds$share) # a semester
solved <- runif(300) < pmin(1, kinds$self_help[q] * help_scale) # <4>
kinds$asked <- tabulate(q, 6)
kinds$reach_TA <- tabulate(q[!solved], 6)
print(kinds[, c("kind", "asked", "reach_TA")], row.names = FALSE)
cat(sum(kinds$reach_TA), "of 300 questions reach the TA\n")

par(mar = c(4, 15, 1, 1))
barplot(t(as.matrix(kinds[6:1, c("reach_TA", "asked")])), # <5>
  beside = TRUE,
  horiz = TRUE, las = 1, names.arg = kinds$kind[6:1],
  cex.names = 0.7, col = c("#d6604d", "grey80"),
  xlab = "Questions in a semester"
)

# Annotations
# 1. The page's control: how well the self-help steps (the book, a friend) work.
# 2. Fixes the random numbers so the run is reproducible.
# 3. Rachel's six kinds of confusion, with how common each is and how often its self-help step resolves it.
# 4. Which of a semester's 300 questions get resolved before they reach the teaching assistant.
# 5. Questions asked and questions that reach the TA, by kind. The taxonomy routes each kind to the right first step.
