from flask_sqlalchemy import SQLAlchemy
from datetime import datetime

db = SQLAlchemy()

class Task(db.Model):
    __tablename__ = 'tbl_tasks'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(255), nullable=False)  # Task name
    priority = db.Column(db.String(50), nullable=False, default="low")  # Priority: low, medium, high
    category = db.Column(db.String(50), nullable=False, default="personal")  # Category: work, health, etc.
    due_date = db.Column(db.DateTime, nullable=True)  # Due date and time
    is_completed = db.Column(db.Boolean, default=False)  # Completion status
    completed_date = db.Column(db.DateTime, nullable=True)  # Completion timestamp
    created_at = db.Column(db.DateTime, default=datetime.utcnow)  # Record creation timestamp
    user_id = db.Column(db.String(36), nullable=False) # User ID

    def __repr__(self):
        return f"<Task {self.name}, Priority: {self.priority}, Completed: {self.is_completed}>"
