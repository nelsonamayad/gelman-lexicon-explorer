# The transitive property of money: wealth buys a hearing on any topic.
w <- 1 # weight the audience gives to wealth # <1>
set.seed(155) # <2>

investor <- rep(c(FALSE, TRUE), each = 100)
expertise <- ifelse(investor, rnorm(200, -1, 1), rnorm(200, 1, 1)) # <3>
wealth <- ifelse(investor, rnorm(200, 2, 0.7), rnorm(200, 0, 0.7))
cred <- expertise + w * wealth + rnorm(200, 0, 0.5) # <4>
heard <- rank(-cred) <= 20 # the 20 most-heard voices # <5>
best <- rank(-expertise) <= 20 # the 20 who know most
cat(sum(heard & investor), " of the 20 most-heard voices are tech ",
  "investors\nAverage expertise: most heard ",
  round(mean(expertise[heard]), 2), ", most expert ",
  round(mean(expertise[best]), 2), "\n",
  sep = ""
)

plot(expertise, cred, # <6>
  pch = ifelse(heard, 19, 1),
  col = ifelse(investor, "#d6604d", "#2166ac"),
  xlab = "Expertise on the topic", ylab = "Credibility with audience"
)
legend("topleft", c("Domain expert", "Tech investor", "Filled: most heard"),
  col = c("#2166ac", "#d6604d", "black"), pch = c(19, 19, 19),
  bty = "n"
)

# Annotations
# 1. The page's control: how much weight the audience gives to wealth.
# 2. Fixes the random numbers so the run is reproducible.
# 3. On this topic the domain experts know more and the tech investors know less.
# 4. Credibility with the audience: expertise plus w times wealth. The money's prestige passes to the speaker.
# 5. The 20 voices that get heard.
# 6. Credibility against expertise, the most-heard voices filled. With w above zero, the investors are heard on a topic they know least about.
