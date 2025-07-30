import os
import logging
import smtplib
from email.message import EmailMessage
from datetime import datetime, timedelta
import csv

# Configuration
TODO_FILE = 'todos.csv'
LOG_FILE = 'todo_app.log'
SMTP_SERVER = 'smtp.example.com'
SMTP_PORT = 587
EMAIL_ADDRESS = 'your_email@example.com'
EMAIL_PASSWORD = 'your_password'

# Set up logging
logging.basicConfig(filename=LOG_FILE, level=logging.INFO)

def send_email(subject, body, to_address):
    try:
        msg = EmailMessage()
        msg['Subject'] = subject
        msg['From'] = EMAIL_ADDRESS
        msg['To'] = to_address
        msg.set_content(body)

        with smtplib.SMTP(SMTP_SERVER, SMTP_PORT) as server:
            server.starttls()
            server.login(EMAIL_ADDRESS, EMAIL_PASSWORD)
            server.send_message(msg)
        logging.info(f'Email sent: {subject} to {to_address}')
    except Exception as e:
        logging.error(f'Error sending email: {e}')

def load_todos():
    todos = []
    if os.path.exists(TODO_FILE):
        with open(TODO_FILE, mode='r', newline='') as file:
            reader = csv.reader(file)
            for row in reader:
                todos.append(row)
    return todos

def save_todos(todos):
    with open(TODO_FILE, mode='w', newline='') as file:
        writer = csv.writer(file)
        for todo in todos:
            writer.writerow(todo)

def add_todo(task, user_email):
    todos = load_todos()
    todos.append([task, 'incomplete', str(datetime.now())])
    save_todos(todos)
    send_email('Task Created', f'Your new task "{task}" has been created.', user_email)

def complete_todo(task, user_email):
    todos = load_todos()
    for i, todo in enumerate(todos):
        if todo[0] == task:
            todos[i][1] = 'complete'
            save_todos(todos)
            send_email('Task Completed', f'Congratulations! You have completed the task "{task}".', user_email)
            break

def upcoming_deadlines(user_email):
    todos = load_todos()
    now = datetime.now()
    deadline_in_a_week = now + timedelta(days=7)
    reminders = []
    
    for todo in todos:
        if todo[1] == 'incomplete':
            task_creation_time = datetime.fromisoformat(todo[2])
            reminder_time = task_creation_time + timedelta(days=7)
            if reminder_time <= deadline_in_a_week:
                reminders.append(todo[0])

    if reminders:
        send_email('Upcoming Deadlines', 'Upcoming deadlines for your tasks: ' + ', '.join(reminders), user_email)

def main():
    logging.info('Starting Todo application')
    user_email = 'user@example.com' 

    try:
        add_todo('Buy groceries', user_email)
        add_todo('Finish project report', user_email)
        complete_todo('Buy groceries', user_email)
        upcoming_deadlines(user_email)
    except Exception as e:
        logging.error(f'Error in main: {e}')

if __name__ == "__main__":
    main()