import sqlite3
from datetime import datetime, timedelta

DB_NAME = "habit_tracker.db"


def get_connection(db_name=DB_NAME):
    """Establishes and returns a database connection with foreign keys enabled."""
    conn = sqlite3.connect(db_name)
    conn.execute("PRAGMA foreign_keys = ON;")
    conn.row_factory = sqlite3.Row
    return conn


def init_db(db_name=DB_NAME):
    """Initializes SQLite database tables for habits and tracking logs."""
    with get_connection(db_name) as conn:
        cursor = conn.cursor()


        # Habits table supporting category and habit_type ("build" vs "break")
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS habits (
                habit_id TEXT PRIMARY KEY,
                name TEXT NOT NULL,
                periodicity TEXT NOT NULL,
                category TEXT NOT NULL DEFAULT 'General',
                habit_type TEXT NOT NULL DEFAULT 'build',
                created_at TEXT NOT NULL
            );
        """)

        # Tracker completion logs table
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS tracker_logs (
                log_id INTEGER PRIMARY KEY AUTOINCREMENT,
                habit_id TEXT NOT NULL,
                completed_at TEXT NOT NULL,
                FOREIGN KEY (habit_id) REFERENCES habits (habit_id) ON DELETE CASCADE
            );
        """)
        conn.commit()


def add_habit(habit, db_name=DB_NAME):
    """Inserts a new habit into the habits table."""
    created_at = getattr(habit, "created_at", None) or datetime.now().isoformat()
    category = getattr(habit, "category", "General")
    habit_type = getattr(habit, "habit_type", "build")

    with get_connection(db_name) as conn:
        conn.execute(
            """
            INSERT INTO habits (habit_id, name, periodicity, category, habit_type, created_at)
            VALUES (?, ?, ?, ?, ?, ?)
            """,
            (habit.habit_id, habit.name, habit.periodicity, category, habit_type, created_at),
        )
        conn.commit()


def get_all_habits(db_name=DB_NAME):
    """Fetches all tracked habits from the database."""
    with get_connection(db_name) as conn:
        cursor = conn.execute(
            "SELECT habit_id, name, periodicity, category, habit_type, created_at FROM habits"
        )
        return [dict(row) for row in cursor.fetchall()]


def log_completion(habit_id: str, timestamp=None, db_name=DB_NAME):
    """Logs a task completion timestamp for a specific habit."""
    completed_at = timestamp or datetime.now().isoformat()
    with get_connection(db_name) as conn:
        conn.execute(
            "INSERT INTO tracker_logs (habit_id, completed_at) VALUES (?, ?)",
            (habit_id, completed_at),
        )
        conn.commit()


def get_logs_for_habit(habit_id, db_name=DB_NAME):
    """Retrieves all completion timestamps for a given habit ID."""
    with get_connection(db_name) as conn:
        cursor = conn.execute(
            """
            SELECT completed_at FROM tracker_logs 
            WHERE habit_id = ? 
            ORDER BY completed_at ASC
            """,
            (habit_id,),
        )
        
        rows = cursor.fetchall()
        return [row[0] if isinstance(row, (tuple, list)) else row["completed_at"] for row in rows]


def delete_habit(habit_id, db_name=DB_NAME):
    """Deletes a habit and cascades deletion to its completion logs."""
    with get_connection(db_name) as conn:
        conn.execute("DELETE FROM habits WHERE habit_id = ?", (habit_id,))
        conn.commit()


def load_predefined_data(db_name=DB_NAME):
    """Resets database and loads sample habits with historical logs."""
    with get_connection(db_name) as conn:
        conn.execute("DELETE FROM tracker_logs")
        conn.execute("DELETE FROM habits")
        conn.commit()

    from habit import Habit

    sample_habits = [
        Habit("h_01", "Gym classes", "daily", "Fitness", "build"),
        Habit("h_02", "Work on Projects", "daily", "Productivity", "build"),
        Habit("h_03", "Meditation", "daily", "Mindfulness", "build"),
        Habit("h_04", "Weekly Grocery Shopping", "weekly", "Health", "build"),
        Habit("h_05", "Limit Junk Food", "daily", "Health", "break"),
        Habit("h_06", "Socialize with Friends", "weekly", "Social", "build"),
    ]

    for habit in sample_habits:
        add_habit(habit, db_name)

    today = datetime.now()
    # Generate logs for h_01 (Daily Exercise) for the past 28 days
    for i in range(28):
        date_str = (today - timedelta(days=27 - i)).strftime("%Y-%m-%d %H:%M:%S")
        log_completion("h_01", date_str, db_name)

    # Generate logs for h_02 (Read 20 Pages) with a missed day on the 10th day
    for i in [10, 9, 8, 2, 1, 0]:
        date_str = (today - timedelta(days=i)).strftime("%Y-%m-%d %H:%M:%S")
        log_completion("h_02", date_str, db_name)

    # 3. h_04: 4 weekly completions (logged once per week over 4 weeks)
    for i in [21, 14, 7, 0]:
        date_str = (today - timedelta(days=i)).strftime("%Y-%m-%d %H:%M:%S")
        log_completion("h_04", date_str, db_name)