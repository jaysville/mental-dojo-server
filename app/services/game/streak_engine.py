from datetime import datetime, timedelta


def update_streak(last_active, current_streak: int):
    """
    Streak rules:
    - +1 if within 24h
    - reset if broken
    """

    if not last_active:
        return 1

    now = datetime.utcnow()

    if now - last_active <= timedelta(hours=24):
        return current_streak + 1

    return 1