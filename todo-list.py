import mysql.connector

# Establish a connection to the MySQL database named 'todo_list'
db = mysql.connector.connect(
    host='localhost',
    port=4306,      # Port number where MySQL is running (change if necessary)
    user='root',    # MySQL username
    password='',    # MySQL password (if any)
    database='todo_list'  # The name of the database to connect to
)

def add_task(task_id, task_name, description):
    """
    Adds a new task to the database.
    
    Parameters:
    - task_id: Unique identifier for the task.
    - task_name: The name/title of the task.
    - description: Details about the task.
    
    The function first checks if a task with the same task_id already exists.
    If not, it inserts the new task into the 'tasks' table.
    """
    # Create a cursor to execute SQL queries
    cursor = db.cursor()
    
    # Check if a task with this task_id already exists in the database
    sql = "SELECT * FROM tasks WHERE id = %s"
    val = (task_id,)
    cursor.execute(sql, val)
    result = cursor.fetchone()  # Retrieve one record if it exists
    
    if result is not None:
        # A task with the provided ID already exists, so we exit the function.
        print("Task with this ID already exists!")
        return

    # Insert the new task into the tasks table if it does not exist
    sql = "INSERT INTO tasks (id, task_name, description) VALUES (%s, %s, %s)"
    val = (task_id, task_name, description)
    cursor.execute(sql, val)
    db.commit()  # Commit the transaction to save the changes
    print("Task added successfully!")


def view_tasks():
    """
    Retrieves and displays all tasks from the 'tasks' table.
    """
    # Create a cursor to execute SQL queries
    cursor = db.cursor()
    sql = "SELECT * FROM tasks"
    cursor.execute(sql)
    tasks = cursor.fetchall()  # Fetch all tasks from the table
    
    if tasks:
        # Loop through each task and print its details
        for task in tasks:
            # Assuming the 'tasks' table columns are ordered as:
            # id, task_name, description, is_completed
            completed_status = 'Yes' if task[3] else 'No'
            print(f"Task ID: {task[0]}, Task Name: {task[1]}, Description: {task[2]}, Completed: {completed_status}")
    else:
        print("No Tasks in the Database")


def mark_completed(task_id):
    """
    Marks the specified task as completed.
    
    Parameter:
    - task_id: The unique identifier of the task to be marked as completed.
    """
    # Create a cursor for executing SQL queries
    cursor = db.cursor()
    # Update the 'is_completed' status to 1 (true) for the specified task
    sql = "UPDATE tasks SET is_completed = 1 WHERE id = %s"
    val = (task_id,)
    cursor.execute(sql, val)
    db.commit()  # Save changes to the database
    print("Task marked as completed!")


def update_task(task_id, task_name, description):
    """
    Updates the name and description of an existing task.
    
    Parameters:
    - task_id: The unique identifier of the task to be updated.
    - task_name: The new task name.
    - description: The new task description.
    """
    # Create a cursor to execute SQL queries
    cursor = db.cursor()
    sql = "UPDATE tasks SET task_name = %s, description = %s WHERE id = %s"
    val = (task_name, description, task_id)
    cursor.execute(sql, val)
    db.commit()  # Commit the update
    print("Task details updated successfully!")


def delete_task(task_id):
    """
    Deletes the task with the specified task_id from the database.
    
    Parameter:
    - task_id: The unique identifier of the task to delete.
    """
    # Create a cursor to execute SQL commands
    cursor = db.cursor()
    sql = "DELETE FROM tasks WHERE id = %s"
    val = (task_id,)
    cursor.execute(sql, val)
    db.commit()  # Commit the deletion
    print("Task deleted successfully!")


if __name__ == "__main__":
    # Main loop for the to-do list application
    while True:
        # Display the menu options
        print("\n--- To-Do List ---")
        print("1. Add Task")
        print("2. View Tasks")
        print("3. Mark Task as Completed")
        print("4. Update Task Details")
        print("5. Delete Task")
        print("6. Exit")

        # Get the user's choice as an integer
        choice = int(input("Enter your choice: "))

        if choice == 1:
            # Get task details from the user and add the task
            task_id = input("Enter the task id: ")
            task_name = input("Enter the task name: ")
            description = input("Enter the task description: ")
            add_task(task_id, task_name, description)

        elif choice == 2:
            # Display all tasks stored in the database
            print("\n--- Tasks ---")
            view_tasks()

        elif choice == 3:
            # Get the task ID from the user and mark it as completed
            task_id = int(input("Enter the task ID to mark as completed: "))
            mark_completed(task_id)

        elif choice == 4:
            # Get updated details and update the task in the database
            task_id = int(input("Enter the task ID to update: "))
            task_name = input("Enter the new task name: ")
            description = input("Enter the new task description: ")
            update_task(task_id, task_name, description)

        elif choice == 5:
            # Get the task ID and delete the task from the database
            task_id = int(input("Enter the task ID to delete: "))
            delete_task(task_id)

        elif choice == 6:
            # Exit the application loop
            print("Exiting...")
            break

        else:
            # Inform the user if the input choice is invalid
            print("Invalid choice. Please try again.")
