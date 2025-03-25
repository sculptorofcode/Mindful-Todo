import uuid
from flask import jsonify, Blueprint, session
from datetime import datetime, timedelta
from models import Task

weekly_progress_bp = Blueprint('weekly_progress', __name__)

def get_user_id():
    if 'user_id' not in session:
        session['user_id'] = str(uuid.uuid4())  # Generate a new UUID if no user_id in session
    return session['user_id']

@weekly_progress_bp.route('/api/weekly-progress', methods=['GET'])
def get_weekly_progress():
    today = datetime.utcnow()
    start_of_week = today - timedelta(days=today.weekday())
    
    tasks_completed = {(start_of_week + timedelta(days=i)).date(): 0 for i in range(7)}
    
    tasks = Task.query.filter(Task.is_completed == True).filter(Task.user_id == get_user_id()).all()
    
    for task in tasks:
        if task.completed_date:
            completed_day = task.completed_date.date()
            if completed_day in tasks_completed:
                tasks_completed[completed_day] += 1
    
    data = list(tasks_completed.values())
    categories = ['Mon', 'Tue', 'Wed', 'Thu', 'Fri', 'Sat', 'Sun']

    return jsonify({
        'categories': categories,
        'data': data
    })
