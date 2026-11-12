# Research Incumbency Rule: once published, a flaw has to be much worse to
# be corrected.
t_pre <- 1.5 # severity that blocks publication in review # <1>
t_post <- 3 # severity needed to correct after publication
p_notice <- 0.5 # chance a reviewer notices a flaw
set.seed(89) # <2>

s <- rexp(5000, rate = 0.8) # severity of each paper's worst flaw
blocked <- runif(5000) < p_notice & s > t_pre # <3>
corrected <- !blocked & s > t_post # <4>
status <- ifelse(blocked, "Rejected in review",
  ifelse(corrected, "Corrected after publication",
    ifelse(s > t_pre, "Published; serious flaw persists",
      "Published; minor or no flaw"
    )
  )
)
counts <- table(status)
print(counts)

par(mar = c(4, 15, 1, 1))
barplot(counts, # <5>
  horiz = TRUE, las = 1, cex.names = 0.75,
  col = "#2166ac", xlab = "Papers (of 5000)"
)

# Annotations
# 1. The page's controls: the flaw severity that blocks publication, the severity needed to force a correction afterwards, and how often a reviewer notices a flaw.
# 2. Fixes the random numbers so the run is reproducible.
# 3. Before publication, a noticed flaw above the review threshold blocks the paper.
# 4. After publication, only a much worse flaw gets corrected: the incumbent result holds the ground.
# 5. What happened to 5,000 papers. Most serious flaws that slipped past review stay in the literature.
