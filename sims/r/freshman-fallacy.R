# The Freshman Fallacy: an experiment on college students only.
gamma <- -0.015 # change in the treatment effect per year of age # <1>
set.seed(43) # <2>

effect <- function(age) 0.5 + gamma * (age - 20)
age <- runif(600, 18, 22) # the experiment: ages 18 to 22 # <3>
z <- rbinom(600, 1, 0.5) # randomized treatment
y <- effect(age) * z + rnorm(600)
est <- mean(y[z == 1]) - mean(y[z == 0]) # <4>
pop_effect <- mean(effect(runif(5000, 18, 80))) # ages 18 to 80 # <5>

cat("Experiment's estimate:", round(est, 2), "\n")
cat("Population-average effect:", round(pop_effect, 2), "\n")

curve(effect, 18, 80, # <6>
  lwd = 2, col = "#2166ac", xlab = "Age",
  ylab = "Treatment effect"
)
rect(18, -10, 22, 10, col = adjustcolor("#2166ac", 0.1), border = NA)
abline(h = est, col = "#2166ac", lty = 2)
abline(h = pop_effect, col = "#d6604d", lty = 2)

# Annotations
# 1. The page's control: how much the treatment effect changes per year of age.
# 2. Fixes the random numbers so the run is reproducible.
# 3. The experiment's subjects are all college students, aged 18 to 22.
# 4. The experiment's estimate, which is unbiased for its own subjects.
# 5. The average effect in the population of interest, aged 18 to 80.
# 6. The effect by age, with the experiment's age range shaded. The two dashed lines differ because the effect varies with a characteristic the sample lacks.
