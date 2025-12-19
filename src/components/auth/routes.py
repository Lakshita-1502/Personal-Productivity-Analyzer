from flask import Blueprint, Flask, render_template, url_for, request, jsonify, redirect, session
from extensions import db

auth_bp = Blueprint("auth", __name__)

@auth_bp.route("/login", methods=["GET", "POST"])
def login():
    cursor=db.cursor(dictionary=True)
    if request.method=="POST":
        userName=request.form.get("userName")
        password=request.form.get("password")
        if userName and password:
            cursor.execute("select id, user_name from users where user_name = %s and password = %s", 
                           (userName,password))
            user=cursor.fetchone()
            if user:
                session["user_id"]=user["id"]
                session["user_name"]=user["user_name"]
                return redirect('/')
        return redirect('/login')
    cursor.close()
    return render_template('login.html')

@auth_bp.route("/register", methods=["GET", "POST"])
def register():
    cursor=db.cursor(dictionary=True)
    if request.method=="POST":
        userName=request.form.get("userName")
        emailId=request.form.get("emailId")
        password=request.form.get("password")
        if userName and emailId and password:
            cursor.execute("insert into users (user_name, email_id, password) values (%s, %s, %s)",
                           (userName, emailId, password))
            db.commit()
        return redirect('/login')
    cursor.close()
    return render_template('register.html')

@auth_bp.route("/logout")
def logout():
    session.clear()
    return redirect('/')

