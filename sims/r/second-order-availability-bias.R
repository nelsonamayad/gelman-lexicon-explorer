# Second-Order Availability Bias: your own circle is not the country.
my_state <- 38 # your state (1 = poorest, 40 = richest) # <1>
set.seed(16) # <2>

# 40 states, 400 voters each. Income matters a lot in poor states and
# hardly at all in rich ones.
state <- rep(1:40, each = 400)
wealth <- (state - 1 - 19.5) / 20 # -1 .. 1
slope <- 0.9 - 0.85 * (wealth + 1) / 2 # <3>
inc <- rnorm(16000, wealth, 1)
vote <- rbinom(16000, 1, plogis(-0.4 * wealth + slope * inc))

mine <- which(state == my_state)[1:200] # your acquaintances # <4>
cat("Slope of vote on income among your acquaintances: ",
  round(coef(lm(vote[mine] ~ inc[mine]))[[2]], 3), "\nIn the whole ",
  "country: ", round(coef(lm(vote ~ inc))[[2]], 3), "\n",
  sep = ""
)

bin <- cut(inc, seq(-3, 3, by = 0.75))
plot(seq(-2.625, 2.625, by = 0.75), tapply(vote, bin, mean), # <5>
  type = "b",
  pch = 19, col = "#2166ac", ylim = c(0, 1), xlab = "Income",
  ylab = "Share voting for the party"
)
bin_mine <- cut(inc[mine], seq(-3, 3, by = 0.75))
points(seq(-2.625, 2.625, by = 0.75), tapply(vote[mine], bin_mine, mean),
  type = "b", pch = 19, col = "#d6604d"
)
legend("topleft", c("Whole country", "Your acquaintances"),
  pch = 19,
  col = c("#2166ac", "#d6604d"), bty = "n"
)

# Annotations
# 1. The page's control: which of 40 states, from poorest to richest, you live in.
# 2. Fixes the random numbers so the run is reproducible.
# 3. Income predicts the vote strongly in poor states and hardly at all in rich ones.
# 4. Your acquaintances: 200 people from your own state.
# 5. Vote against income for the whole country and for your acquaintances. Your circle is a sample from one state, and the national pattern can be the opposite of what it shows.
