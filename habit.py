from datetime import datetime
class Habit:

    """Represents a periodic habit task and handles checking it off.

    Attributes:
        habit_id (str): Unique identifier for the habit.
        name (str): Short description of the habit task.
        periodicity (str): Frequency of task ('daily' or 'weekly').
        created_at (str): ISO timestamp of habit creation.
    """

    def __init__(
        self,
        habit_id: str,
        name: str,
        periodicity: str,
        category: str = "General",
        habit_type: str = "build",
        created_at: str = None,
    ):
        if periodicity not in ["daily", "weekly"]:
            raise ValueError("Periodicity must be either 'daily' or 'weekly'")
        if habit_type not in ["build", "break"]:
            raise ValueError("Habit type must be either 'build' or 'break'")

        self.habit_id = habit_id
        self.name = name
        self.periodicity = periodicity
        self.category = category
        self.habit_type = habit_type
        self.created_at = created_at or datetime.now().isoformat()

    def complete_task(self, timestamp: str = None) -> dict:
        """Generates a check-off record when the user completes this habit task."""
        return {
            "habit_id": self.habit_id,
            "completed_at": timestamp or datetime.now().isoformat(),
        }