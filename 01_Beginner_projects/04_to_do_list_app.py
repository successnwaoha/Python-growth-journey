tasks = []

# Normalize tasks: ensure every task is a dict {"title": str, "completed": bool}
# This handles legacy lists that may contain plain strings.
tasks = [t if isinstance(t, dict) else {"title": t, "completed": False} for t in tasks]

def display_header():
    print("+---------------------------------+")
    print("|          To-Do List App         |")
    print("+---------------------------------+\n")

def display_menu():
    print("Menu")
    print("----")
    print("1) Add Task")
    print("2) View Tasks")
    print("3) Remove Task")
    print("4) Mark Task as Completed")
    print("5) Exit")

def print_tasks(tasks):
    print("\nYour Tasks:")
    if not tasks:
        print("  (No tasks yet)")
        return
    for idx, task in enumerate(tasks, start=1):
        title = task.get("title", "")
        completed = task.get("completed", False)
        status = "✓" if completed else " "
        print(f"  {idx:2}. [{status}] {title}")
    print()

display_header()
while True:
    display_menu()
    choice = input("Choose an option (1-5): ")
    if choice == '1':
        task = input("Enter the task title to add: ").strip()
        if not task:
            print("Task title cannot be empty. Try again.\n")
            continue
        # store tasks as dicts so we can track completion status
        tasks.append({"title": task, "completed": False})
        print(f"Task '{task}' added to the list.\n")
    elif choice == '2':
        print_tasks(tasks)
    elif choice == '3':
        if tasks:
            print("\nYour Tasks:")
            print_tasks(tasks)
            try:
                task_num = int(input("Enter the task number to remove: "))
                if 1 <= task_num <= len(tasks):
                    removed_task = tasks.pop(task_num - 1)
                    removed_title = removed_task["title"]
                    print(f"Task '{removed_title}' removed from the list.\n")
                else:
                    print("Invalid task number.\n")
            except ValueError:
                print("Please enter a valid number.\n")
        else:
            print("Your to-do list is empty.\n")
    elif choice == '4':
        if tasks:
            print_tasks(tasks)
            try:
                task_num = int(input("Enter the task number to mark as completed: "))
                if 1 <= task_num <= len(tasks):
                    tasks[task_num - 1]["completed"] = True
                    print(f"Task '{tasks[task_num - 1]['title']}' marked as completed.\n")
                else:
                    print("Invalid task number.\n")
            except ValueError:
                print("Please enter a valid number.\n")
        else:
            print("Your to-do list is empty.\n")
    elif choice == '5':
        print("Exiting To-Do List App...... Goodbye!")
        break
        
    else:
        print("Invalid choice. Please select a valid option (1-5).\n")