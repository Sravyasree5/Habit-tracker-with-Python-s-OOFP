from datetime import datetime


def get_all_tracked_habits(habits: list) -> list:
    """Returns a list of all habit names."""
    return list(map(lambda h: h["name"], habits))

def get_habits_by_category(habits: list, category: str) -> list:
    """Returns habits filtered by a specific category."""
    return list(filter(lambda h: h["category"].lower() == category.lower(), habits))

def get_habits_by_periodicity(habits: list, periodicity: str) -> list:
    """Filters habits matching 'daily' or 'weekly' periodicity."""
    return list(filter(lambda h: h["periodicity"] == periodicity, habits))


def calculate_streak(logs: list, periodicity: str) -> int:
    """Calculates the longest consecutive period streak from completion logs."""
    if not logs:
        return 0

    # Parse and sort timestamps
    parsed_dates = []
    for log in logs:
        # Extract timestamp string whether log is a string or a dict
        ts = log["completed_at"] if isinstance(log, dict) else log
        
        if isinstance(ts, str):
            try:
                parsed_dates.append(datetime.fromisoformat(ts).date())
            except ValueError:
                # Ignores non-date strings like 'test_habit_tracker.db'
                continue

    dates = sorted(set(parsed_dates))
    
    if not dates:
        return 0 
    max_streak = 1
    current_streak = 1

    max_gap = 1 if periodicity == "daily" else 7

    for i in range(1, len(dates)):
        day_diff = (dates[i] - dates[i-1]).days

        if day_diff <= max_gap:
            # Add 1 for each consecutive transition
            current_streak += 1
        else:
            # Gap detected - reset streak back to 1
            current_streak = 1

        if current_streak > max_streak:
            max_streak = current_streak

    return max_streak

def get_longest_streak_for_habit(
    habit_id: str, logs: list, periodicity: str
) -> int:
    """Returns the maximum streak count achieved by a specific habit."""
    return calculate_streak(logs, periodicity)


def get_longest_streak_all_habits(
    habits: list, db_get_logs_func, db_name=None
) -> tuple:
    """Finds the overall longest streak among all tracked habits."""
    longest_streak = 0
    top_habit = None

    for habit in habits:
        logs = (
            db_get_logs_func(habit["habit_id"], db_name)
            if db_name
            else db_get_logs_func(habit["habit_id"])
        )
        streak = calculate_streak(logs, habit["periodicity"])
        if streak > longest_streak:
            longest_streak = streak
            top_habit = habit["name"]

    return top_habit, longest_streak