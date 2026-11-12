# The Chestertonian Principle: extreme skepticism is a form of credulity.
import numpy as np
import matplotlib.pyplot as plt

survey_bias = 0.08  # survey bias, known in direction and correctable
alt_bias = 0.12     # spread of the alternative source's unknown bias
rng = np.random.default_rng(65)

truth = rng.uniform(0.1, 0.9, 500)  # 500 questions about attitudes
survey = (truth - survey_bias * rng.normal(1, 0.3, 500)
          + rng.normal(0, 0.03, 500))
corrected = survey + survey_bias  # model-based correction
alternative = truth + rng.normal(0, alt_bias, 500) + rng.normal(0, 0.03, 500)

rmse = {"Trusts raw survey": survey, "Corrects survey biases": corrected,
        "Extreme skeptic": alternative}
rmse = {k: np.sqrt(np.mean((v - truth) ** 2)) for k, v in rmse.items()}
for k, v in rmse.items():
    print(f"{k}: root-mean-square error {v:.3f}")

plt.barh(list(rmse)[::-1], list(rmse.values())[::-1],
         color=["#d6604d", "#2166ac", "0.7"])
plt.xlabel("Root-mean-square error")
plt.tight_layout()
plt.show()
