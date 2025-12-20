from flask import Blueprint, Flask, render_template, url_for, request, jsonify, redirect, session
from extensions import db

tasks_bp = Blueprint("tasks", __name__)

@tasks_bp.route("/")
def home():
    return render_template("pages/dashboard.html", page="dashboard")

@tasks_bp.route("/add-task", methods=["GET", "POST"])
def taskForm():   
    cursor=db.cursor(dictionary=True)
    if request.method=="POST":
        taskDesc=request.form.get("taskName")
        taskValue=request.form.get("valuePoint")
        if taskDesc and taskValue:
            cursor.execute("insert into tasks (name, value_points) values (%s, %s)", 
                           (taskDesc, int(taskValue)))
            db.commit()
    cursor.execute("select * from tasks")
    tasks=cursor.fetchall()
    cursor.close()
    return render_template('pages/taskForm.html', tasks=tasks, page="task")

@tasks_bp.route("/update", methods=["POST"])
def update():
    cursor=db.cursor()
    data=request.get_json()
    cursor.execute("update tasks set completed=%s where id=%s", (data["completed"], data["id"]))
    db.commit()
    cursor.close()
    return jsonify(success=True)

@tasks_bp.route("/delete/<int:task_id>", methods=["POST"])
def delete_task(task_id):
    cursor=db.cursor()
    cursor.execute("delete from tasks where id=%s", (task_id,))
    db.commit()
    cursor.close()
    return redirect('/add-task')
