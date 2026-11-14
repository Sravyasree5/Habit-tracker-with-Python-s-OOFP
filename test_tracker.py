import pytest
import database
import analytics
from habit import Habit

TEST_DB = "test_habit_tracker.db"


@pytest.fixture(autouse=True)
def setup_test_db():
    database.init_db(TEST_DB)
    database.load_predefined_data(TEST_DB)


def test_habit_creation():
    h = Habit("h_test", "Read Book", "daily", "Education", "build")
    assert h.name == "Read Book"
    assert h.periodicity == "daily"
    assert h.category == "Education"
    assert h.habit_type == "build"


def test_invalid_periodicity():
    with pytest.raises(ValueError):
        Habit("h_err", "Bad Habit", "monthly")


# --- NEW: Tests validation for invalid habit type ---
def test_invalid_habit_type():
    with pytest.raises(ValueError):
        Habit("h_err", "Bad Habit", "daily", "General", "invalid_type")

def test_habit_completion():
    initial_logs = database.get_logs_for_habit("h_01", TEST_DB)
    initial_count = len(initial_logs)

    database.log_completion("h_01", db_name=TEST_DB)

    updated_logs = database.get_logs_for_habit("h_01", db_name=TEST_DB)
    assert len(updated_logs) == initial_count + 1

def test_streak_calculation():
    # 28 consecutive days should yield a 28-day streak
    logs = database.get_logs_for_habit("h_01", db_name=TEST_DB)
    streak = analytics.calculate_streak(logs, "daily")
    assert streak == 28


def test_broken_streak():
    logs = database.get_logs_for_habit("h_02", db_name=TEST_DB)
    streak = analytics.calculate_streak(logs, "daily")
    assert streak == 3

def test_predefined_habits_categories_and_types():
    habits = database.get_all_habits(db_name=TEST_DB)
    
    # Verify total count of sample_habits
    assert len(habits) == 6
    
    # Check specific sample habit attributes from database
    h01 = next(h for h in habits if h["habit_id"] == "h_01")
    assert h01["category"] == "Fitness"
    assert h01["habit_type"] == "build"

    h05 = next(h for h in habits if h["habit_id"] == "h_05")
    assert h05["category"] == "Health"
    assert h05["habit_type"] == "break"