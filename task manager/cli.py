import click
from flask import Flask
from models import db, Task

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///tasks.db'
db.init_app(app)

# Ensure DB exists
with app.app_context():
    db.create_all()

@click.group()
def cli():
    """Task Manager CLI"""
    pass

@cli.command()
@click.argument('title')
@click.argument('priority')
@click.argument('deadline')
def add(title, priority, deadline):
    """Add a new task from CLI"""
    with app.app_context():
        new_task = Task(title=title, priority=priority, deadline=deadline)
        db.session.add(new_task)
        db.session.commit()
        click.echo(f"✅ Task '{title}' added successfully!")

@cli.command()
def list():
    """List all tasks"""
    with app.app_context():
        tasks = Task.query.all()
        if not tasks:
            click.echo("No tasks found.")
        else:
            for task in tasks:
                click.echo(f"[{task.id}] {task.title} | {task.priority} | {task.deadline}")

@cli.command()
@click.argument('task_id', type=int)
def delete(task_id):
    """Delete a task by ID"""
    with app.app_context():
        task = Task.query.get(task_id)
        if task:
            db.session.delete(task)
            db.session.commit()
            click.echo(f"🗑️ Task '{task.title}' deleted successfully!")
        else:
            click.echo("Task not found.")

if __name__ == '__main__':
    cli()
