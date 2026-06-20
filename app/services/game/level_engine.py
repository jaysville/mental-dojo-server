import math


# -----------------------------
# GLOBAL LEVEL SYSTEM
# -----------------------------
def calculate_global_level(xp: int) -> int:
    """
    Exponential leveling curve:
    level = sqrt(xp / 100)
    """

    return max(1, int(math.sqrt(xp / 100)) + 1)


# -----------------------------
# FACULTY LEVEL SYSTEM
# -----------------------------
def calculate_faculty_level(xp: int) -> int:
    """
    Slower curve than global level (forces mastery)
    """

    return max(1, int(math.sqrt(xp / 150)) + 1)


# -----------------------------
# NEXT LEVEL XP THRESHOLD
# -----------------------------
def xp_for_next_level(level: int) -> int:
    """
    How much XP needed for next level
    """
    return (level + 1) ** 2 * 100