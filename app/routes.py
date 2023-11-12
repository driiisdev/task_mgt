from app import app
from app.models import User, Task
from flask import request, jsonify, session
from datetime import datetime
from werkzeug.security import generate_password_hash, check_password_hash


@app.route('/api')
def api():
    response = jsonify({'message': 'api ok'})
    response.headers['Access-Control-Allow-Origin'] = '*'
    return response

# Signup endpoint
@app.route("/api/signup", methods=["POST"])
def signup():
    data = request.get_json()

    # Validate the data
    if not data or not data["username"] or not data["email"] or not data["password"]:
        return jsonify({"error": "Invalid data."}), 400

    # Check if the user already exists
    user = User.query.filter_by(email=data["email"]).first()
    if user is not None:
        return jsonify({"error": "User already exists."}), 409

    # Create the new user
    user = User(data["username"], data["email"], generate_password_hash(data["password"]))
    user.save()

    # Return a success message
    return jsonify({"message": "User created successfully."}), 201

# Login endpoint
@app.route("/api/login", methods=["POST"])
def login():
    data = request.get_json()

    # Validate the data
    if not data or not data["email"] or not data["password"]:
        return jsonify({"error": "Invalid data."}), 400

    # Check if the user exists
    user = User.query.filter_by(email=data["email"]).first()
    if user is None:
        return jsonify({"error": "User does not exist."}), 404

    # Check the password
    if not check_password_hash(user.password, data["password"]):
        return jsonify({"error": "Incorrect password."}), 401

    # Log the user in
    session["user_id"] = user.id

    # Return a success message
    return jsonify({"message": "User logged in successfully."}), 200

# Logout endpoint
@app.route("/api/logout", methods=["GET"])
def logout():
    # Log the user out
    session.pop("user_id", None)

    # Return a success message
    return jsonify({"message": "User logged out successfully."}), 200


@app.route('/api/tasks', methods=['GET', 'POST'])
def tasks():
    if request.method == 'GET':
        # Get all tasks
        tasks = Task.query.all()
        return jsonify(tasks), 200
    elif request.method == 'POST':
        # Create a new task
        task = Task(
            title=request.json['title'],
            description=request.json['description'],
            due_date=datetime.datetime.strptime(request.json['due_date'], '%Y-%m-%d'),
            completed=request.json['completed']
        )
        task.save()
        return jsonify(task)
    
@app.route('/api/tasks/<task_id>', methods=['GET', 'PUT', 'DELETE'])
def task(task_id):
    task = Task.query.get(task_id)
    if not task:
        return jsonify({'error': 'Task not found'}), 404

    if request.method == 'GET':
        # Get the task
        return jsonify(task)
    elif request.method == 'PUT':
        # Update the task
        task.title=request.json['title']
        task.description=request.json['description']

        # Convert the deadline to a datetime object
        task.due_date=datetime.datetime.strptime(request.json['due_date'], '%Y-%m-%d')
        task.completed=request.json['completed']

        task.save()
        return jsonify(task)
    elif request.method == 'DELETE':
        # Delete the task
        task.delete()
        return jsonify({'success': 'Task deleted'})

@app.route('/api/tasks/search', methods=['GET', 'POST'])
def search():
    # Search tasks by title
    title=request.args.get("title")
    tasks = Task.query.filter(Task.title.like(f"%{title}%"))

    # Return the filtered tasks
    return tasks

@app.route('/api/tasks/filter', methods=['GET', 'POST'])
def tasks_filter():
    # Convert the deadline to a datetime object
    deadline=request.args.get("deadline")
    deadline = datetime.date.fromisoformat(deadline)

    # Filter the tasks by deadline date
    tasks = Task.query.filter(Task.deadline >= deadline)

    # Return the filtered tasks
    return tasks
