import uuid
from flask import jsonify, Blueprint, session
from collections import Counter
from models import Task

task_distribution_bp = Blueprint('task_distribution', __name__)

def get_user_id():
    if 'user_id' not in session:
        session['user_id'] = str(uuid.uuid4())  # Generate a new UUID if no user_id in session
    return session['user_id']

@task_distribution_bp.route('/api/task-distribution', methods=['GET'])
def get_task_distribution():
    tasks = Task.query.filter(Task.user_id == get_user_id()).all()
    categories = [task.category for task in tasks]
    category_counts = Counter(categories)

    categories_list = ['Personal', 'Work', 'Health', 'Learning']
    distribution = [category_counts.get(category.lower(), 0) for category in categories_list]

    return jsonify({
        'categories': categories_list,
        'distribution': distribution
    })
