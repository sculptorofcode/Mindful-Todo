from flask import jsonify, Blueprint
from collections import Counter
from models import Task

task_distribution_bp = Blueprint('task_distribution', __name__)

@task_distribution_bp.route('/api/task-distribution', methods=['GET'])
def get_task_distribution():
    tasks = Task.query.all()
    categories = [task.category for task in tasks]
    category_counts = Counter(categories)

    categories_list = ['Personal', 'Work', 'Health', 'Learning']
    distribution = [category_counts.get(category.lower(), 0) for category in categories_list]

    return jsonify({
        'categories': categories_list,
        'distribution': distribution
    })
