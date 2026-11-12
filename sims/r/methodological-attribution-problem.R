# The Methodological Attribution Problem: credit the analyst, not the method.
method_effect <- 0.1 # true effect of the fancy method # <1>
selection <- 2 # how strongly skill predicts using it
set.seed(40) # <2>

skill <- rnorm(1000)
uses_method <- rbinom(1000, 1, plogis(selection * skill)) # <3>
quality <- method_effect * uses_method + skill + rnorm(1000, 0, 0.5)

naive <- mean(quality[uses_method == 1]) - mean(quality[uses_method == 0]) # <4>
adjusted <- coef(lm(quality ~ uses_method + skill))[["uses_method"]] # <5>
cat("Naive credit to the method:", round(naive, 2), "\n")
cat("Adjusted for skill: ", round(adjusted, 2), " (true effect ",
  method_effect, ")\n",
  sep = ""
)

boxplot(quality ~ uses_method, # <6>
  names = c("Standard method", "Fancy method"),
  col = c("grey70", "#2166ac"), xlab = "",
  ylab = "Quality of the analysis"
)

# Annotations
# 1. The page's controls: the fancy method's true effect on quality, and how strongly skilled analysts gravitate to it.
# 2. Fixes the random numbers so the run is reproducible.
# 3. Skilled analysts are more likely to use the fancy method.
# 4. The credit the method gets if you compare analyses that used it with those that didn't.
# 5. The credit it deserves, once the analyst's skill is accounted for.
# 6. Quality by method. The gap is mostly the analysts, not the method.
