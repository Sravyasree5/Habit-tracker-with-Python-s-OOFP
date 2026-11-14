import questionary
import database
import analytics
from habit import Habit
import quotes

def main():
    database.init_db()
    print("\n Welcome! to the Habit tracker CLI.")
    print(f"Quote of the day: {quotes.get_motivation()}\n")

    while True:
        # Replaced manual print statements and raw input() with questionary select menu
        choice_str = questionary.select(
            "--- Habit Tracker Menu ---",
            choices=[
                "1. List all habits",
                "2. List habits by periodicity",
                "3. Add a new habit",
                "4. Check-off a habit",
                "5. Analyze longest streak for a habit",
                "6. Analyze overall longest streak across all habits",
                "7. Delete a habit",
                "8. Reset and load 4-week sample test data",
                "9. Exit"
            ]
        ).ask()

        # Handle edge case if user cancels with Ctrl+C
        if not choice_str:
            print("Bye! Have a great day!")
            break

        # Extract the menu option number (e.g., "1. List all habits" -> "1")
        choice = choice_str.split(".")[0]

        if choice == "1":
            habits = database.get_all_habits()
            print("\nTracked Habits:")
            if not habits:
                print(" - No habits found. Try adding one or loading sample data (Option 8).")
            for h in habits:
                print(
                    f" - [{h['habit_id']}] {h['name']} ({h['periodicity'].capitalize()}) | "
                    f"Category: {h['category']} | Type: {h['habit_type'].capitalize()} | "
                    f"Created: {h['created_at'][:10]}"
                )

        elif choice == "2":
            period = questionary.select(
                "Select periodicity to filter by:",
                choices=["daily", "weekly"]
            ).ask().lower()
            
            habits = database.get_all_habits()
            filtered = analytics.get_habits_by_periodicity(habits, period)
            print(f"\n{period.capitalize()} Habits:")
            if not filtered:
                print(f" - No {period} habits found.")
            for h in filtered:
                print(
                    f" - [{h['habit_id']}] {h['name']} | "
                    f"Category: {h['category']} | Type: {h['habit_type'].capitalize()} | "
                    f"Created: {h['created_at'][:10]}"
                )

        elif choice == "3":
            hid = f"h_{len(database.get_all_habits()) + 1:02d}"
            name = questionary.text("Enter habit name:").ask().strip()
            if not name:
                print("Error: Habit name cannot be empty.")
                continue
                
            period = questionary.select(
                "Enter periodicity:",
                choices=["daily", "weekly"]
            ).ask().lower()
            
            category = questionary.text("Enter category (default 'General'):", default="General").ask().strip() or "General"
            habit_type = questionary.select(
                "Enter type:",
                choices=["build", "break"]
            ).ask().lower()

            try:
                new_h = Habit(hid, name, period, category, habit_type)
                database.add_habit(new_h)
                print(f"Success! Habit '{name}' created with ID '{hid}'.")
            except ValueError as e:
                print(f"Error: {e}")

        elif choice == "4":
            habits = database.get_all_habits()
            if not habits:
                print("No habits available to check off.")
                continue
            
            habit_choices = [f"{h['habit_id']}: {h['name']} ({h['periodicity']})" for h in habits]
            selected_str = questionary.select(
                "Select a habit to check off:",
                choices=habit_choices
            ).ask()
            
            hid = selected_str.split(":")[0].strip()
            database.log_completion(hid)
            print(f"Task for habit '{hid}' checked off!")

        elif choice == "5":
            habits = database.get_all_habits()
            if not habits:
                print("No habits available to analyze.")
                continue
            
            habit_choices = [f"{h['habit_id']}: {h['name']}" for h in habits]
            selected_str = questionary.select(
                "Select a habit for streak analysis:",
                choices=habit_choices
            ).ask()
            
            hid = selected_str.split(":")[0].strip()
            target = next((h for h in habits if h["habit_id"] == hid), None)
            if target:
                logs = database.get_logs_for_habit(hid)
                streak = analytics.get_longest_streak_for_habit(
                    hid, logs, target["periodicity"]
                )
                print(
                    f"Longest streak for '{target['name']}': {streak} period(s)"
                )
            else:
                print("Habit not found.")

        elif choice == "6":
            habits = database.get_all_habits()
            top_h, max_s = analytics.get_longest_streak_all_habits(
                habits, database.get_logs_for_habit
            )
            if top_h:
                print(f"Top Habit: '{top_h}' with a streak of {max_s} period(s)!")
            else:
                print("No completions recorded yet.")

        elif choice == "7":
            habits = database.get_all_habits()
            if not habits:
                print("No habits available to delete.")
            else:
                habit_choices = [f"{h['habit_id']}: {h['name']}" for h in habits]
                selected_str = questionary.select(
                    "Select a habit to delete:",
                    choices=habit_choices
                ).ask()
                
                hid = selected_str.split(":")[0].strip()
                target = next((h for h in habits if h["habit_id"] == hid), None)
                
                if target:
                    confirm = questionary.confirm(f"Are you sure you want to delete '{target['name']}'?").ask()
                    if confirm:
                        database.delete_habit(target['habit_id'])
                        print(f"Habit '{target['name']}' deleted successfully!")
                    else:
                        print("Deletion cancelled.")

        elif choice == "8":
            database.load_predefined_data()
            print("Successfully loaded 6 predefined habits and 4-week sample fixture logs!")

        elif choice == "9":
            print("Bye! Have a great day!")
            break


if __name__ == "__main__":
    main()