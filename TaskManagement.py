import tkinter as tk
from tkinter import messagebox, simpledialog
from datetime import datetime

class Task:
    def __init__(self, task_id, title, description, status, estimated_hours):
        self.task_id = task_id
        self.title = title
        self.description = description
        self.status = status
        self.estimated_hours = estimated_hours

class Sprint:
    def __init__(self, sprint_id, name, start_date, end_date):
        self.sprint_id = sprint_id
        self.name = name
        self.start_date = start_date
        self.end_date = end_date
        self.tasks = []

    # function to add task to the sprint
    def add_task(self, task):
        self.tasks.append(task)

    # function to remove task from the sprint
    def remove_task(self, task_id):
        self.tasks = [task for task in self.tasks if task.task_id != task_id]

    # function to calculate burndown count
    def calculate_burndown(self):
        total_hours = sum(task.estimated_hours for task in self.tasks)
        days_remaining = (self.end_date - datetime.now().date()).days
        if days_remaining <= 0:
            return 0, total_hours
        return days_remaining, total_hours

    # function to display tasks in the sprint
    def display_tasks(self):
        if not self.tasks:
            return "No tasks in this sprint."
        return "\n".join(f"{task.task_id}: {task.title} - {task.status} ({task.estimated_hours} hours)" for task in self.tasks)

class TaskManagementSystem:
    def __init__(self, root):
        self.root = root
        self.root.title("Task Management System")

        self.tasks = {}
        self.sprints = {}

        self.create_widgets()

    def create_widgets(self):
        # Buttons for Task Management
        tk.Button(self.root, text="Add Task", command=self.add_task).pack(pady=5)
        tk.Button(self.root, text="Update Task", command=self.update_task).pack(pady=5)
        tk.Button(self.root, text="Delete Task", command=self.delete_task).pack(pady=5)

        # Buttons for Sprint Management
        tk.Button(self.root, text="Add Sprint", command=self.add_sprint).pack(pady=5)
        tk.Button(self.root, text="Update Sprint", command=self.update_sprint).pack(pady=5)
        tk.Button(self.root, text="Delete Sprint", command=self.delete_sprint).pack(pady=5)
        tk.Button(self.root, text="Show Sprint Tasks", command=self.show_sprint_tasks).pack(pady=5)

        # Button to see Burndown Count for a Sprint
        tk.Button(self.root, text="Show Burndown Count", command=self.show_burndown_count).pack(pady=5)

    # funtion with all input box and all for adding a task
    def add_task(self):
        task_id = simpledialog.askstring("Input", "Enter Task ID:")
        title = simpledialog.askstring("Input", "Enter Task Title:")
        description = simpledialog.askstring("Input", "Enter Task Description:")
        status = simpledialog.askstring("Input", "Enter Task Status (TO DO, In Progress, Done):")
        estimated_hours = simpledialog.askfloat("Input", "Enter Estimated Hours:")
        sprint_id = simpledialog.askstring("Input", "Enter Sprint ID to associate with this task:")

        if sprint_id in self.sprints:
            task = Task(task_id, title, description, status, estimated_hours)
            self.tasks[task_id] = task
            self.sprints[sprint_id].add_task(task)
            messagebox.showinfo("Success", "Task added successfully!")
        else:
            messagebox.showerror("Error", "Sprint ID not found!")

    # function with all input box and all for updating a task
    def update_task(self):
        task_id = simpledialog.askstring("Input", "Enter Task ID to update:")
        if task_id in self.tasks:
            title = simpledialog.askstring("Input", "Enter new Task Title:", initialvalue=self.tasks[task_id].title)
            description = simpledialog.askstring("Input", "Enter new Task Description:", initialvalue=self.tasks[task_id].description)
            status = simpledialog.askstring("Input", "Enter new Task Status (TO DO, In Progress, Done):", initialvalue=self.tasks[task_id].status)
            estimated_hours = simpledialog.askfloat("Input", "Enter new Estimated Hours:", initialvalue=self.tasks[task_id].estimated_hours)
            self.tasks[task_id] = Task(task_id, title, description, status, estimated_hours)
            messagebox.showinfo("Success", "Task updated successfully!")
        else:
            messagebox.showerror("Error", "Task ID not found!")

    # function with all input box and all for deleting a task
    def delete_task(self):
        task_id = simpledialog.askstring("Input", "Enter Task ID to delete:")
        if task_id in self.tasks:
            # Remove task from associated sprint
            for sprint in self.sprints.values():
                sprint.remove_task(task_id)
            del self.tasks[task_id]
            messagebox.showinfo("Success", "Task deleted successfully!")
        else:
            messagebox.showerror("Error", "Task ID not found!")

    # function with all input box and all for adding a sprint
    def add_sprint(self):
        sprint_id = simpledialog.askstring("Input", "Enter Sprint ID:")
        name = simpledialog.askstring("Input", "Enter Sprint Name:")
        start_date = simpledialog.askstring("Input", "Enter Start Date (YYYY-MM-DD):")
        end_date = simpledialog.askstring("Input", "Enter End Date (YYYY-MM-DD):")
        sprint = Sprint(sprint_id, name, datetime.strptime(start_date, "%Y-%m-%d").date(), datetime.strptime(end_date, "%Y-%m-%d").date())
        self.sprints[sprint_id] = sprint
        messagebox.showinfo("Success", "Sprint added successfully!")

    # function with all input box and all for updating a sprint
    def update_sprint(self):
        sprint_id = simpledialog.askstring("Input", "Enter Sprint ID to update:")
        if sprint_id in self.sprints:
            name = simpledialog.askstring("Input", "Enter new Sprint Name:", initialvalue=self.sprints[sprint_id].name)
            start_date = simpledialog.askstring("Input", "Enter new Start Date (YYYY-MM-DD):", initialvalue=self.sprints[sprint_id].start_date.strftime("%Y-%m-%d"))
            end_date = simpledialog.askstring("Input", "Enter new End Date (YYYY-MM-DD):", initialvalue=self.sprints[sprint_id].end_date.strftime("%Y-%m-%d"))
            self.sprints[sprint_id] = Sprint(sprint_id, name, datetime.strptime(start_date, "%Y-%m-%d").date(), datetime.strptime(end_date, "%Y-%m-%d").date())
            messagebox.showinfo("Success", "Sprint updated successfully!")
        else:
            messagebox.showerror("Error", "Sprint ID not found!")
    # function for deleing a task based on sprint id
    def delete_sprint(self):
        sprint_id = simpledialog.askstring("Input", "Enter Sprint ID to delete:")
        if sprint_id in self.sprints:
            del self.sprints[sprint_id]
            messagebox.showinfo("Success", "Sprint deleted successfully!")
        else:
            messagebox.showerror("Error", "Sprint ID not found!")

    # function to show all tasks in a sprint based on spring ID
    def show_sprint_tasks(self):
        sprint_id = simpledialog.askstring("Input", "Enter Sprint ID to view tasks:")
        if sprint_id in self.sprints:
            tasks_display = self.sprints[sprint_id].display_tasks()
            messagebox.showinfo("Sprint Tasks", tasks_display)
        else:
            messagebox.showerror("Error", "Sprint ID not found!")

    # function to show burndown count based on sprint ID
    def show_burndown_count(self):
        sprint_id = simpledialog.askstring("Input", "Enter Sprint ID to view burndown count:")
        if sprint_id in self.sprints:
            days_remaining, total_hours = self.sprints[sprint_id].calculate_burndown()
            messagebox.showinfo("Burndown Count", f"Days Remaining: {days_remaining}\nTotal Estimated Hours: {total_hours}")
        else:
            messagebox.showerror("Error", "Sprint ID not found!")

if __name__ == "__main__":
    root = tk.Tk()
    app = TaskManagementSystem(root)
    root.mainloop()