from dataclasses import dataclass
import math


@dataclass
class XPResult:
    xp: int


# -----------------------------
# BASE XP TABLE
# -----------------------------
BASE_XP = {
    "easy": 10,
    "medium": 20,
    "hard": 35
}


# -----------------------------
# XP CALCULATION ENGINE
# -----------------------------
def calculate_xp(difficulty: str, is_correct: bool, streak: int, accuracy: float = 1.0):
    """
    XP ECONOMY RULES:
    - correctness required
    - streak gives multiplier (capped)
    - difficulty scales base XP
    - accuracy improves reward
    """

    if not is_correct:
        return XPResult(xp=0)

    base = BASE_XP.get(difficulty, 10)

    # 🔥 streak multiplier (soft cap at 2.5x)
    streak_multiplier = min(1 + (streak * 0.1), 2.5)

    # 🧠 skill precision bonus
    accuracy_multiplier = 0.8 + (accuracy * 0.4)  # 0.8 → 1.2 range

    # 📈 exponential smoothing (prevents inflation)
    xp = base * streak_multiplier * accuracy_multiplier

    return XPResult(xp=int(math.floor(xp)))