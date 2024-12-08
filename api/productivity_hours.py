from flask import jsonify, Blueprint, session
from datetime import datetime, timedelta
from models import Task

productivity_hours_bp = Blueprint('productivity_hours', __name__)

def get_user_id():
    if 'user_id' not in session:
        session['user_id'] = str(uuid.uuid4())  # Generate a new UUID if no user_id in session
    return session['user_id']

@productivity_hours_bp.route('/api/productivity-hours', methods=['GET'])
def get_productivity_hours():
    hours = [f"{hour}AM" if hour < 12 else f"{hour-12}PM" for hour in range(6, 12)] + \
            [f"{hour}PM" for hour in range(12, 12 + 6)] + \
            [f"{hour}AM" for hour in range(12, 12 + 6)]
    hour_counts = {hour: 0 for hour in hours}

    tasks = Task.query.filter(Task.is_completed == True).filter(Task.user_id == get_user_id()).all()
    for task in tasks:
        if task.completed_date:
            hour = task.completed_date.hour
            if 6 <= hour < 24:
                hour_label = hours[hour - 6]
            else:
                hour_label = hours[hour + 18]
            hour_counts[hour_label] += 1
    
    data = list(hour_counts.values())
    categories = list(hour_counts.keys())

    return jsonify({
        'categories': categories,
        'data': data
    })
