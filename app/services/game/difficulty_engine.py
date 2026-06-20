from app.models.faculty_progress import FacultyProgress

def calculate_next_difficulty(faculty_progress: FacultyProgress):
    if faculty_progress.attempts < 5:
        return "easy"

    accuracy = (faculty_progress.correct / faculty_progress.attempts) * 100
    recent_accuracy = faculty_progress.recent_accuracy
    streak = faculty_progress.streak

    if accuracy > 80 and recent_accuracy > 75 and streak >= 3:
        return "hard"

    if accuracy > 50:
        return "medium"

    return "easy"