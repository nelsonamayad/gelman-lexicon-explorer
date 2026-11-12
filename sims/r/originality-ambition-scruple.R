# Originality, ambition, and lack of scruple: who rises to the top?
reward <- 1 # how much citations reward exaggeration # <1>
set.seed(151) # <2>

N <- 5000
O <- rnorm(N)
A <- rnorm(N)
S <- rnorm(N) # originality, ambition, scruple
exaggeration <- pmax(0, A - S) # <3>
cites <- O + reward * exaggeration + rnorm(N, 0, 0.5) # <4>
top <- rank(-cites) <= 100 # the top 2% by citations # <5>

means <- rbind(
  "Top 2% by citations" = c(
    mean(O[top]), mean(A[top]),
    mean(S[top])
  ),
  "Everyone else" = c(
    mean(O[!top]), mean(A[!top]),
    mean(S[!top])
  )
)
colnames(means) <- c("Originality", "Ambition", "Scruple")
print(round(means, 2))

barplot(means, # <6>
  beside = TRUE, col = c("#d6604d", "grey70"),
  ylab = "Average (standard units)", legend.text = TRUE,
  args.legend = list(x = "topright", bty = "n")
)
abline(h = 0)

# Annotations
# 1. The page's control: how much citations reward exaggeration.
# 2. Fixes the random numbers so the run is reproducible.
# 3. Exaggeration happens when ambition exceeds scruple.
# 4. Citations reward originality, and exaggeration too.
# 5. The top 2% by citations.
# 6. The top group against everyone else on originality, ambition and scruple. Selection on citations selects for the combination.
