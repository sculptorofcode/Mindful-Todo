import uuid
from flask import Flask, request, jsonify, render_template, redirect, url_for, session
from dotenv import load_dotenv
import os
from models import Task, db
from flask_migrate import Migrate
import werkzeug
from datetime import datetime
import requests
from apscheduler.schedulers.background import BackgroundScheduler

from api.productivity_hours import productivity_hours_bp
from api.task_distribution import task_distribution_bp
from api.weekly_progress import weekly_progress_bp
from api.analytics import analytics_bp

load_dotenv()

app = Flask(__name__)
app.secret_key = os.getenv('SECRET_KEY')  # Needed to use sessions securely
migrate = Migrate()

SERVICE_URI = os.getenv("SERVICE_URI")

app.config['SQLALCHEMY_DATABASE_URI'] = SERVICE_URI
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db.init_app(app)
migrate.init_app(app, db)

app.register_blueprint(productivity_hours_bp)
app.register_blueprint(task_distribution_bp)
app.register_blueprint(weekly_progress_bp)
app.register_blueprint(analytics_bp)

def input_date(date):
    return datetime.strptime(date, '%d-%m-%Y %H:%M') if date else None

def output_date(date):
    return date.strftime('%d-%m-%Y %I:%M %p') if date else 'No due date'

# Helper to get the user ID from session
def get_user_id():
    if 'user_id' not in session:
        session['user_id'] = str(uuid.uuid4())  # Generate a new UUID if no user_id in session
    return session['user_id']

@app.route('/')
def home():
    tasks = Task.query.filter_by(user_id=get_user_id()).all()  # Filter tasks by user_id
    return render_template('index.html', tasks=tasks)

@app.route('/analytics')
def analytics():
    return render_template('analytics.html')

@app.route('/tasks', methods=['GET'])
def tasks():
    try:
        # Pagination parameters
        start = int(request.args.get('start', 0))
        length = int(request.args.get('length', 10))
        order_column = request.args.get('order[0][column]', 0)
        order_direction = request.args.get('order[0][dir]', 'asc')
        search_value = request.args.get('search[value]', None)
        draw = int(request.args.get('draw', 1))

        # Base query
        tasks_query = Task.query.filter_by(user_id=get_user_id())
        tasks_query = tasks_query.filter(Task.is_completed == False)  # Filter out completed tasks
        total_records = tasks_query.count()  # Total unfiltered records

        # Apply search filter
        if search_value:
            tasks_query = tasks_query.filter(
                Task.name.ilike(f'%{search_value}%') |
                Task.priority.ilike(f'%{search_value}%') |
                Task.category.ilike(f'%{search_value}%')
            )

        filtered_records = tasks_query.count()  # Total records after filtering

        # Apply sorting
        sort_column_map = {
            'id': Task.id,
            'name': Task.name,
            'priority': Task.priority,
            'category': Task.category,
            'due_date': Task.due_date
        }
        sort_column = sort_column_map.get(order_column, Task.id)  # Default sort by ID
        if order_direction == 'desc':
            sort_column = sort_column.desc()

        tasks_query = tasks_query.order_by('due_date', sort_column)

        # Apply pagination
        tasks = tasks_query.offset(start).limit(length).all()

        # Format tasks for DataTables
        tasks_data = []
        for idx, task in enumerate(tasks, start=start + 1):
            tasks_data.append({
                'sl_no': idx,
                'id': task.id,
                'name': task.name.capitalize(),
                'priority': task.priority.capitalize(),
                'category': task.category.capitalize(),
                'due_date': output_date(task.due_date),
                'is_completed': task.is_completed,
            })

        # Return JSON response
        return jsonify({
            'draw': draw,
            'recordsTotal': total_records,  # Total unfiltered records
            'recordsFiltered': filtered_records,  # Total records after filtering
            'data': tasks_data  # Paginated and formatted task data
        })
    except Exception as e:
        return jsonify({'error': str(e)}), 400

@app.route('/add', methods=['POST'])
def add_task():
    try:
        task_name = request.form['name']
        priority = request.form['priority']
        category = request.form['category']
        due_date = request.form['due_date']
        user_id = get_user_id()  # Get the user ID from session

        # Create a new task and associate it with the user
        new_task = Task(
            name=task_name,
            priority=priority,
            category=category,
            due_date=datetime.strptime(due_date, '%d-%m-%Y %H:%M') if due_date else None,
            user_id=user_id  # Associate the task with the user ID
        )

        db.session.add(new_task)
        db.session.commit()

        return jsonify({
            'id': new_task.id,
            'name': new_task.name,
            'priority': new_task.priority,
            'category': new_task.category,
            'due_date': new_task.due_date.strftime('%d-%m-%Y %H:%M') if new_task.due_date else 'No due date',
            'is_completed': new_task.is_completed,
            'message': 'Task added successfully'
        }), 201
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': str(e)}), 400

@app.route('/complete/<int:task_id>', methods=['POST'])
def complete_task(task_id):
    try:
        task = Task.query.get_or_404(task_id)
        task.is_completed = True
        task.completed_date = datetime.now()
        db.session.commit()

        return jsonify({
            'id': task.id,
            'name': task.name,
            'priority': task.priority,
            'category': task.category,
            'due_date': task.due_date.strftime('%d-%m-%Y %H:%M') if task.due_date else 'No due date',
            'is_completed': task.is_completed
        }), 200
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': str(e)}), 400

@app.route('/delete/<int:task_id>', methods=['POST'])
def delete_task(task_id):
    try:
        task = Task.query.get_or_404(task_id)
        db.session.delete(task)
        db.session.commit()

        return jsonify({'success': True, 'id': task_id}), 200
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': str(e)}), 400

@app.errorhandler(Exception)
def handle_error(e):
    if isinstance(e, werkzeug.exceptions.MethodNotAllowed):
        return redirect(url_for('home'))
    else:
        return jsonify({"error": str(e), "status" : "error"}), 500

if __name__ == '__main__':
    with app.app_context():
        db.create_all()
    app.run(debug=False)
