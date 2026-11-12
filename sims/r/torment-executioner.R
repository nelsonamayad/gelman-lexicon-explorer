# Torment executioner: what a paraphrasing tool does to technical terms.
p <- 0.6 # probability each word is swapped # <1>
set.seed(130) # <2>

synonyms <- c( # <3>
  pain = "torment", killer = "executioners",
  intensity = "concentration", repetitive = "tedious",
  movements = "developments", artificial = "counterfeit",
  intelligence = "consciousness", deep = "profound",
  big = "colossal", data = "information", random = "irregular",
  forest = "woodland", network = "organization",
  mean = "normal", error = "blunder", signal = "flag",
  noise = "commotion"
)
phrases <- c(
  "pain killer", "intensity of pain", "repetitive movements",
  "artificial intelligence", "deep learning", "big data",
  "random forest", "neural network", "mean square error",
  "signal to noise"
)
spin <- function(ph) { # <4>
  w <- strsplit(ph, " ")[[1]]
  swap <- w %in% names(synonyms) & runif(length(w)) < p
  w[swap] <- synonyms[w[swap]]
  paste(w, collapse = " ")
}
spun <- sapply(phrases, spin) # <5>
print(data.frame(term = phrases, spun = unname(spun)), row.names = FALSE)
cat("A two-word term survives intact ", round(100 * (1 - p)^2),
  "% of the time\n",
  sep = ""
)

# Annotations
# 1. The page's control: the probability that the spinner swaps each word.
# 2. Fixes the random numbers so the run is reproducible.
# 3. A small synonym dictionary of the kind a paraphrasing tool uses. Pain killer becomes torment executioner.
# 4. The spinner: swap each word it knows with its synonym, with probability p.
# 5. Ten technical phrases after spinning. A k-word term survives only if every word is left alone, so longer terms are mangled more often.
