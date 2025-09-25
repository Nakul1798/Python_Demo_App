from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

class Task(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(200), nullable=False)
    priority = db.Column(db.String(50), nullable=False)
    deadline = db.Column(db.String(50), nullable=True)

    def __repr__(self):
        return f"<Task {self.title}>"
