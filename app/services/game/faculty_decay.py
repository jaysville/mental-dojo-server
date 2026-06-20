def decay_recent_stats(faculty_progress):
    faculty_progress.recent_correct = int(faculty_progress.recent_correct * 0.6)
    faculty_progress.recent_attempts = int(faculty_progress.recent_attempts * 0.6)

    if faculty_progress.recent_attempts > 0:
        faculty_progress.recent_accuracy = int(
            (faculty_progress.recent_correct / faculty_progress.recent_attempts) * 100
        )
    else:
        faculty_progress.recent_accuracy = 0