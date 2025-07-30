import os
import csv
import logging
from datetime import datetime

# Configure logging
logging.basicConfig(filename='todo_list.log', level=logging.DEBUG, format='%(asctime)s - %(levelname)s - %(message)s')

class Task:
    def __init__(self, description, due_date=None, priority=None, category=None):
        self.description = description
        self.due_date = due_date
        self.priority = priority
        self.category = category
        self.completed = False

    def __str__(self):
        return f"[{'X' if self.completed else ' '}] {self.description} - Due: {self.due_date}, Priority: {self.priority}, Category: {self.category}"

class TodoList:
    def __init__(self, filename):
        self.filename = filename
        self.tasks = []
        self.load_tasks()

    def load_tasks(self):
        if os.path.exists(self.filename):
            with open(self.filename, mode='r', newline='') as file:
                reader = csv.reader(file)
                for row in reader:
                    if row:
                        task = Task(description=row[0], due_date=row[1], priority=row[2], category=row[3])
                        task.completed = row[4] == 'True'
                        self.tasks.append(task)
            logging.info("Tasks loaded successfully from file.")
        else:
            logging.warning("Task file does not exist, starting with an empty task list.")

    def save_tasks(self):
        with open(self.filename, mode='w', newline='') as file:
            writer = csv.writer(file)
            for task in self.tasks:
                writer.writerow([task.description, task.due_date, task.priority, task.category, task.completed])
        logging.info("Tasks saved successfully to file.")

    def add_task(self, description, due_date, priority, category):
        task = Task(description, due_date, priority, category)
        self.tasks.append(task)
        logging.info(f"Task added: {task}")
        self.save_tasks()

    def delete_task(self, description):
        original_count = len(self.tasks)
        self.tasks = [task for task in self.tasks if task.description != description]
        if len(self.tasks) < original_count:
            logging.info(f"Task deleted: {description}")
            self.save_tasks()
        else:
            logging.warning(f"Task not found for deletion: {description}")

    def update_task(self, description, completed=None):
        for task in self.tasks:
            if task.description == description:
                if completed is not None:
                    task.completed = completed
                    logging.info(f"Task updated: {task}")
                    self.save_tasks()
                return
        logging.warning(f"Task not found for update: {description}")

    def list_tasks(self):
        if not self.tasks:
            logging.info("No tasks available.")
            return "No tasks available."
        return "\n".join(str(task) for task in self.tasks)

def main():
    todo_list = TodoList('tasks.csv')

    todo_list.add_task('Finish project report', '2023-10-30', 'High', 'Work')
    todo_list.add_task('Buy groceries', '2023-10-20', 'Medium', 'Personal')
    todo_list.add_task('Call Mom', None, 'Low', 'Personal')

    print("Current tasks:")
    print(todo_list.list_tasks())

    todo_list.update_task('Buy groceries', completed=True)
    print("Updated tasks:")
    print(todo_list.list_tasks())

    todo_list.delete_task('Call Mom')
    print("Final tasks after deletion:")
    print(todo_list.list_tasks())

if __name__ == "__main__":
    main()