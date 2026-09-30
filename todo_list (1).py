import csv
import os

FILE_NAME = "todo_tasks.csv"


def load_tasks():
    tasks = []
    if os.path.exists(FILE_NAME):
        try:
            with open(FILE_NAME, "r", newline="", encoding="utf-8") as file:
                reader = csv.DictReader(file)
                for row in reader:
                    if all(key in row for key in ["name", "category", "priority", "status"]):
                        tasks.append(row)
        except (OSError, csv.Error) as error:
            print("Error while loading tasks:", error)
    return tasks


def save_tasks(tasks):
    try:
        with open(FILE_NAME, "w", newline="", encoding="utf-8") as file:
            fieldnames = ["name", "category", "priority", "status"]
            writer = csv.DictWriter(file, fieldnames=fieldnames)
            writer.writeheader()
            writer.writerows(tasks)
    except OSError as error:
        print("Error while saving tasks:", error)


def get_priority():
    while True:
        print("\nSelect Priority")
        print("1. High")
        print("2. Medium")
        print("3. Low")
        choice = input("Enter your choice: ").strip()

        if choice == "1":
            return "High"
        elif choice == "2":
            return "Medium"
        elif choice == "3":
            return "Low"
        else:
            print("Invalid choice. Please enter 1, 2, or 3.")


def get_task_number(tasks):
    if not tasks:
        print("\nNo tasks available.")
        return None

    while True:
        try:
            number = int(input("Enter task number: ").strip())
            if 1 <= number <= len(tasks):
                return number - 1
            print(f"Please enter a number between 1 and {len(tasks)}.")
        except ValueError:
            print("Please enter a valid number.")


def add_task(tasks):
    print("\n========== ADD TASK ==========")
    name = input("Enter task name: ").strip()

    if not name:
        print("Task name cannot be empty.")
        return

    category = input("Enter task category: ").strip()
    if not category:
        category = "General"

    priority = get_priority()

    task = {
        "name": name,
        "category": category,
        "priority": priority,
        "status": "Pending"
    }

    tasks.append(task)
    save_tasks(tasks)
    print("\nTask added successfully!")


def view_tasks(tasks):
    print("\n========== YOUR TASKS ==========")

    if not tasks:
        print("No tasks available.")
        return

    for number, task in enumerate(tasks, start=1):
        print(f"\nTask Number: {number}")
        print("Task Name :", task["name"])
        print("Category  :", task["category"])
        print("Priority  :", task["priority"])
        print("Status    :", task["status"])


def edit_task(tasks):
    print("\n========== EDIT TASK ==========")
    index = get_task_number(tasks)

    if index is None:
        return

    task = tasks[index]

    print("\nCurrent Task Details")
    print("Name     :", task["name"])
    print("Category :", task["category"])
    print("Priority :", task["priority"])

    new_name = input(
        "\nEnter new task name (press Enter to keep old name): "
    ).strip()
    if new_name:
        task["name"] = new_name

    new_category = input(
        "Enter new category (press Enter to keep old category): "
    ).strip()
    if new_category:
        task["category"] = new_category

    while True:
        change_priority = input(
            "Do you want to change priority? (y/n): "
        ).strip().lower()

        if change_priority == "y":
            task["priority"] = get_priority()
            break
        elif change_priority in ("n", ""):
            break
        else:
            print("Please enter y or n.")

    save_tasks(tasks)
    print("\nTask updated successfully!")


def complete_task(tasks):
    print("\n========== COMPLETE TASK ==========")
    index = get_task_number(tasks)

    if index is None:
        return

    if tasks[index]["status"] == "Completed":
        print("This task is already completed.")
        return

    tasks[index]["status"] = "Completed"
    save_tasks(tasks)
    print("\nTask marked as completed!")


def delete_task(tasks):
    print("\n========== DELETE TASK ==========")
    index = get_task_number(tasks)

    if index is None:
        return

    print("\nTask selected:", tasks[index]["name"])

    while True:
        confirm = input(
            "Are you sure you want to delete this task? (y/n): "
        ).strip().lower()

        if confirm == "y":
            deleted_task = tasks.pop(index)
            save_tasks(tasks)
            print("\nTask deleted successfully:", deleted_task["name"])
            break
        elif confirm in ("n", ""):
            print("\nDelete operation cancelled.")
            break
        else:
            print("Please enter y or n.")


def task_report(tasks):
    print("\n========== TASK REPORT ==========")

    if not tasks:
        print("No tasks available for report.")
        return

    total_tasks = len(tasks)
    completed_tasks = 0
    pending_tasks = 0
    high_priority = 0
    medium_priority = 0
    low_priority = 0
    categories = {}

    for task in tasks:
        if task["status"] == "Completed":
            completed_tasks += 1
        else:
            pending_tasks += 1

        if task["priority"] == "High":
            high_priority += 1
        elif task["priority"] == "Medium":
            medium_priority += 1
        elif task["priority"] == "Low":
            low_priority += 1

        category = task["category"]
        categories[category] = categories.get(category, 0) + 1

    print("Total Tasks     :", total_tasks)
    print("Completed Tasks :", completed_tasks)
    print("Pending Tasks   :", pending_tasks)

    print("\nPriority Summary")
    print("High Priority   :", high_priority)
    print("Medium Priority :", medium_priority)
    print("Low Priority    :", low_priority)

    print("\nCategory Summary")
    for category, count in categories.items():
        print(f"{category}: {count}")


def main():
    tasks = load_tasks()

    print("\n======================================")
    print("       TO-DO LIST MANAGEMENT SYSTEM")
    print("======================================")

    while True:
        print("\n--------------- MENU ----------------")
        print("1. Add Task")
        print("2. View Tasks")
        print("3. Edit Task")
        print("4. Mark Task as Completed")
        print("5. Delete Task")
        print("6. Task Report")
        print("7. Exit")
        print("-------------------------------------")

        choice = input("Enter your choice: ").strip()

        if choice == "1":
            add_task(tasks)
        elif choice == "2":
            view_tasks(tasks)
        elif choice == "3":
            edit_task(tasks)
        elif choice == "4":
            complete_task(tasks)
        elif choice == "5":
            delete_task(tasks)
        elif choice == "6":
            task_report(tasks)
        elif choice == "7":
            print("\nThank you for using the To-Do List!")
            print("Goodbye!")
            break
        else:
            print("\nInvalid choice.")
            print("Please select a number from 1 to 7.")


if __name__ == "__main__":
    main()
