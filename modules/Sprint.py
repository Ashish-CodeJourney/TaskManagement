class Sprint:
    def __init__(self, sprint_id, name, start_date, end_date):
        self.sprint_id = sprint_id
        self.name = name
        self.start_date = start_date
        self.end_date = end_date
        self.tasks = []

    def add_task(self, task):
        self.tasks.append(task)

    def remove_task(self, task_id):
        self.tasks = [task for task in self.tasks if task.task_id != task_id]

    def calculate_burndown(self):
        total_hours = sum(task.estimated_hours for task in self.tasks)
        days_remaining = (self.end_date - datetime.now().date()).days
        if days_remaining <= 0:
            return 0, total_hours
        return days_remaining, total_hours
