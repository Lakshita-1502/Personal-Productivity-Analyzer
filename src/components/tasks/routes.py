from flask import Blueprint, Flask, render_template, url_for, request, jsonify, redirect, session
from extensions import db
from components.auth.routes import login_required

tasks_bp = Blueprint("tasks", __name__)

@tasks_bp.route("/")
def home():
    print("HOME SESSION:", dict(session))
    print("User ID:", session.get('user_id'))
    print("User Name:", session.get('user_name'))
    return render_template("pages/dashboard.html", page="dashboard")    

@tasks_bp.route("/add-task", methods=["GET", "POST"])
@login_required  # Protect this route
def taskForm():   
    cursor = db.cursor(dictionary=True)
    try:
        if request.method == "POST":
            taskDesc = request.form.get("taskName")
            taskValue = request.form.get("valuePoint", type=int)
            user_id = session.get('user_id')
            
            if taskDesc and taskValue and user_id:
                # Add user_id to associate task with logged-in user
                cursor.execute(
                    "INSERT INTO tasks (name, value_points, user_id) VALUES (%s, %s, %s)", 
                    (taskDesc, int(taskValue), user_id)
                )
                db.commit()
        
        # Fetch only tasks for the logged-in user
        user_id = session.get('user_id')
        cursor.execute("SELECT * FROM tasks WHERE user_id = %s", (user_id,))
        tasks = cursor.fetchall()
        
        return render_template('pages/taskForm.html', tasks=tasks, page="task")
    finally:
        cursor.close()

@tasks_bp.route("/update", methods=["POST"])
@login_required  # Protect this route
def update():
    cursor = db.cursor()
    try:
        data = request.get_json()
        user_id = session.get('user_id')
        
        # Ensure user can only update their own tasks
        cursor.execute(
            "UPDATE tasks SET completed=%s WHERE id=%s AND user_id=%s", 
            (data["completed"], data["id"], user_id)
        )
        db.commit()
        return jsonify(success=True)
    except Exception as e:
        db.rollback()
        return jsonify(success=False, error=str(e)), 400
    finally:
        cursor.close()

@tasks_bp.route("/delete/<int:task_id>", methods=["POST"])
@login_required  # Protect this route
def delete_task(task_id):
    cursor = db.cursor()
    try:
        user_id = session.get('user_id')
        
        # Ensure user can only delete their own tasks
        cursor.execute("DELETE FROM tasks WHERE id=%s AND user_id=%s", (task_id, user_id))
        db.commit()
        return redirect('/add-task')
    finally:
        cursor.close()