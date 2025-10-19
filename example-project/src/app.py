"""
TaskFlow - Simple Task Management Web App
Main application file
"""

from flask import Flask, render_template, request, redirect, url_for, flash, jsonify
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime
import os

# Initialize Flask app
app = Flask(__name__)
app.config['SECRET_KEY'] = 'dev-secret-key-change-in-production'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///taskflow.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

# Initialize database
db = SQLAlchemy(app)

# Task Model
class Task(db.Model):
    """Task model representing a single task"""
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(200), nullable=False)
    description = db.Column(db.Text, nullable=True)
    status = db.Column(db.String(20), nullable=False, default='pending')
    priority = db.Column(db.String(20), nullable=False, default='medium')
    due_date = db.Column(db.DateTime, nullable=True)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    def to_dict(self):
        """Convert task to dictionary for JSON serialization"""
        return {
            'id': self.id,
            'title': self.title,
            'description': self.description,
            'status': self.status,
            'priority': self.priority,
            'due_date': self.due_date.isoformat() if self.due_date else None,
            'created_at': self.created_at.isoformat(),
            'updated_at': self.updated_at.isoformat()
        }

    def __repr__(self):
        return f'<Task {self.id}: {self.title}>'


# Routes

@app.route('/')
def index():
    """Main dashboard showing all tasks"""
    # Get filter parameters
    status_filter = request.args.get('status')
    priority_filter = request.args.get('priority')
    
    # Build query
    query = Task.query
    
    if status_filter:
        query = query.filter_by(status=status_filter)
    
    if priority_filter:
        query = query.filter_by(priority=priority_filter)
    
    # Get all tasks
    tasks = query.order_by(Task.created_at.desc()).all()
    
    return render_template('index.html', tasks=tasks)


@app.route('/task/<int:id>')
def task_detail(id):
    """View detailed information for a specific task"""
    task = Task.query.get_or_404(id)
    return render_template('task_detail.html', task=task)


@app.route('/task/create', methods=['GET', 'POST'])
def create_task():
    """Create a new task"""
    if request.method == 'POST':
        title = request.form.get('title')
        description = request.form.get('description')
        priority = request.form.get('priority', 'medium')
        due_date_str = request.form.get('due_date')
        
        # Validate required fields
        if not title:
            flash('Title is required', 'error')
            return redirect(url_for('create_task'))
        
        # Parse due date if provided
        due_date = None
        if due_date_str:
            try:
                due_date = datetime.strptime(due_date_str, '%Y-%m-%d')
            except ValueError:
                flash('Invalid date format', 'error')
                return redirect(url_for('create_task'))
        
        # Create new task
        task = Task(
            title=title,
            description=description,
            priority=priority,
            due_date=due_date
        )
        
        db.session.add(task)
        db.session.commit()
        
        flash('Task created successfully', 'success')
        return redirect(url_for('index'))
    
    return render_template('create_task.html')


@app.route('/task/<int:id>/update', methods=['GET', 'POST'])
def update_task(id):
    """Update an existing task"""
    task = Task.query.get_or_404(id)
    
    if request.method == 'POST':
        task.title = request.form.get('title')
        task.description = request.form.get('description')
        task.status = request.form.get('status')
        task.priority = request.form.get('priority')
        
        due_date_str = request.form.get('due_date')
        if due_date_str:
            try:
                task.due_date = datetime.strptime(due_date_str, '%Y-%m-%d')
            except ValueError:
                flash('Invalid date format', 'error')
                return redirect(url_for('update_task', id=id))
        
        task.updated_at = datetime.utcnow()
        db.session.commit()
        
        flash('Task updated successfully', 'success')
        return redirect(url_for('task_detail', id=id))
    
    return render_template('update_task.html', task=task)


@app.route('/task/<int:id>/delete', methods=['POST'])
def delete_task(id):
    """Delete a task"""
    task = Task.query.get_or_404(id)
    db.session.delete(task)
    db.session.commit()
    
    flash('Task deleted successfully', 'success')
    return redirect(url_for('index'))


@app.route('/task/<int:id>/status', methods=['POST'])
def update_status(id):
    """Quick update task status"""
    task = Task.query.get_or_404(id)
    new_status = request.form.get('status')
    
    if new_status in ['pending', 'in_progress', 'completed', 'cancelled']:
        task.status = new_status
        task.updated_at = datetime.utcnow()
        db.session.commit()
        flash('Status updated successfully', 'success')
    else:
        flash('Invalid status', 'error')
    
    return redirect(url_for('index'))


@app.route('/search')
def search_tasks():
    """Search tasks by title or description"""
    query = request.args.get('q', '')
    
    if len(query) < 2:
        return jsonify([])
    
    tasks = Task.query.filter(
        db.or_(
            Task.title.ilike(f'%{query}%'),
            Task.description.ilike(f'%{query}%')
        )
    ).limit(50).all()
    
    return jsonify([task.to_dict() for task in tasks])


# Initialize database
with app.app_context():
    db.create_all()
    
    # Create sample tasks if database is empty
    if Task.query.count() == 0:
        sample_tasks = [
            Task(
                title='Set up Flask project',
                description='Initialize Flask application with proper structure',
                status='completed',
                priority='high'
            ),
            Task(
                title='Implement task filtering',
                description='Add ability to filter tasks by status and priority',
                status='in_progress',
                priority='high'
            ),
            Task(
                title='Add search functionality',
                description='Implement search feature for finding tasks',
                status='pending',
                priority='medium'
            ),
        ]
        
        for task in sample_tasks:
            db.session.add(task)
        
        db.session.commit()
        print('Sample tasks created')


if __name__ == '__main__':
    app.run(debug=True, port=5000)

