from flask import jsonify, request, Blueprint, session
from datetime import datetime, timedelta
from models import Task  # Assuming Task model is already defined in models.py
from sqlalchemy import func
from sqlalchemy.sql.expression import case

analytics_bp = Blueprint('analytics', __name__)

# Helper functions
def calculate_completion_rate(completed, total):
    return round((completed / total) * 100, 2) if total > 0 else 0

def calculate_on_time_rate(tasks):
    if not tasks:
        return 0
    on_time_count = sum(1 for task in tasks if task.completed_date and task.completed_date <= task.due_date)
    return round((on_time_count / len(tasks)) * 100, 2)

def calculate_avg_completion_time(tasks):
    if not tasks:
        return 0
    total_time = sum((task.completed_date - task.created_at).total_seconds() for task in tasks if task.completed_date)
    avg_time_seconds = total_time / len(tasks) if tasks else 0
    avg_time_hours = round(avg_time_seconds / 3600, 2)
    return avg_time_hours

def get_user_id():
    if 'user_id' not in session:
        session['user_id'] = str(uuid.uuid4())  # Generate a new UUID if no user_id in session
    return session['user_id']

# Endpoint for analytics data
@analytics_bp.route('/api/analytics', methods=['GET'])
def analytics():
    user_id = get_user_id()
    try:
        # Get the time period (default: 7 days)
        days = int(request.args.get('days', 7))
        start_date = datetime.now() - timedelta(days=days)

        # Query tasks
        tasks_query = Task.query.filter(Task.created_at >= start_date)
        tasks_query = tasks_query.filter(Task.user_id == user_id)

        # Total tasks
        total_tasks = tasks_query.count()

        # Completed tasks
        completed_tasks = tasks_query.filter(Task.is_completed == True).all()

        # Completion rate
        completion_rate = calculate_completion_rate(len(completed_tasks), total_tasks)

        # On-time completion rate
        on_time_rate = calculate_on_time_rate(completed_tasks)

        # Average completion time
        avg_completion_time = calculate_avg_completion_time(completed_tasks)

        # Task completion trend (daily counts)
        trend_data = (
            Task.query
            .with_entities(
                func.date(Task.completed_date).label('date'),
                func.count().label('created_count'),
                func.sum(case((Task.completed_date.isnot(None), 1), else_=0)).label('completed_count')
            )
            .filter(Task.user_id == user_id)
            .filter(Task.completed_date >= start_date)
            .group_by(func.date(Task.completed_date))
            .order_by(func.date(Task.completed_date))
            .all()
        )

        dates = [str(row.date) for row in trend_data]
        created_counts = [row.created_count for row in trend_data]
        completed_counts = [row.completed_count for row in trend_data]

        # Category distribution
        category_distribution = (
            Task.query
            .with_entities(Task.category, func.count())
            .filter(Task.user_id == user_id)
            .filter(Task.created_at >= start_date)
            .group_by(Task.category)
            .all()
        )
        categories = [row[0] for row in category_distribution]
        for category in categories:
            categories = [category.capitalize() for category in categories]
        category_counts = [row[1] for row in category_distribution]

        # Priority analysis
        priority_analysis = (
            Task.query
            .with_entities(Task.priority, func.count())
            .filter(Task.user_id == user_id)
            .filter(Task.created_at >= start_date)
            .group_by(Task.priority)
            .all()
        )
        priorities = [row[0] for row in priority_analysis]
        priority_counts = [row[1] for row in priority_analysis]

        # Daily activity pattern (hourly counts)
        activity_pattern = (
            Task.query
            .with_entities(
                func.extract('hour', Task.completed_date).label('hour'),
                func.count()
            )
            .filter(Task.user_id == user_id)
            .filter(Task.completed_date >= start_date)
            .group_by(func.extract('hour', Task.completed_date))
            .order_by(func.extract('hour', Task.completed_date))
            .all()
        )
        hours = [int(row[0]) for row in activity_pattern]
        activity_counts = [row[1] for row in activity_pattern]

        # Build response
        data = {
            'total_tasks': total_tasks,
            'completion_rate': completion_rate,
            'on_time_rate': on_time_rate,
            'avg_completion_time': avg_completion_time,
            'completion_trend': {
                'dates': dates,
                'created': created_counts,
                'completed': completed_counts
            },
            'category_distribution': {
                'categories': categories,
                'values': category_counts
            },
            'priority_analysis': {
                'priorities': priorities,
                'counts': priority_counts
            },
            'activity_pattern': {
                'hours': hours,
                'counts': activity_counts
            }
        }
        return jsonify(data)

    except Exception as e:
        return jsonify({'error': str(e)}), 400
