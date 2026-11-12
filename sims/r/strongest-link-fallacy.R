# Strongest-link Fallacy: a chain of evidence is as strong as all its links.
links <- c( # <1>
  Randomization = 0.98, # randomization was done properly
  Measurement = 0.75, # outcome measures what we care about
  "Power / noise" = 0.6, # estimate isn't noise
  Generalization = 0.65
) # result generalizes to the policy
# Deterministic: no random numbers. If the links are independent, the
# whole chain holds with the product of their probabilities.

chain <- c(links, "Whole chain" = prod(links)) # <2>
print(round(chain, 2))

par(mar = c(4, 8, 1, 1))
barplot(rev(chain), # <3>
  horiz = TRUE, las = 1, xlim = c(0, 1),
  col = c("#d6604d", rep("#2166ac", 4)),
  xlab = "Probability the link holds"
)

# Annotations
# 1. The page's controls: the probability that each link of the argument holds. There is no seed: the model is deterministic.
# 2. If the links are independent, the whole chain holds with the product of their probabilities, which is less than the weakest link.
# 3. Each link and the whole chain. Pointing to the strongest link, the randomization, says nothing about the chain.
