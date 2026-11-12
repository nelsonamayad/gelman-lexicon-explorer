# Torment executioner: what a paraphrasing tool does to technical terms.
import numpy as np

p = 0.6  # probability each word is swapped
rng = np.random.default_rng(130)

synonyms = {"pain": "torment", "killer": "executioners",
            "intensity": "concentration", "repetitive": "tedious",
            "movements": "developments", "artificial": "counterfeit",
            "intelligence": "consciousness", "deep": "profound",
            "big": "colossal", "data": "information", "random": "irregular",
            "forest": "woodland", "network": "organization",
            "mean": "normal", "error": "blunder", "signal": "flag",
            "noise": "commotion"}
phrases = ["pain killer", "intensity of pain", "repetitive movements",
           "artificial intelligence", "deep learning", "big data",
           "random forest", "neural network", "mean square error",
           "signal to noise"]


def spin(phrase):
    return " ".join(synonyms[w] if w in synonyms and rng.uniform() < p
                    else w for w in phrase.split())


for ph in phrases:
    print(f"{ph:25s} -> {spin(ph)}")
print(f"A two-word term survives intact {100 * (1 - p) ** 2:.0f}% of "
      "the time")
