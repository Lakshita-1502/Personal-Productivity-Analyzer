from flask import Blueprint, flash, render_template, url_for, request, redirect, session
from extensions import db
from functools import wraps

auth_bp = Blueprint("auth", __name__)

def login_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if 'user_id' not in session:
            flash('Please log in to access this page.', 'warning')
            return redirect(url_for('auth.login'))
        return f(*args, **kwargs)
    return decorated_function

@auth_bp.route("/login", methods=["GET", "POST"])
def login():
    if "user_id" in session:
        return redirect("/")
    
    if request.method=="POST":
        cursor=db.cursor(dictionary=True)
        try:
            userName=request.form.get("userName")
            password=request.form.get("password")

            if userName and password:
                cursor.execute("select id, user_name from users where user_name = %s and password = %s", 
                            (userName,password))
                user=cursor.fetchone()

                if user:
                    session.clear()
                    session["user_id"]=user["id"]
                    session["user_name"]=user["user_name"]
                    session.permanent=True
                    flash('Login successful!', 'success')
                    return redirect('/')
                else:
                    flash('Invalid username or password', 'error')
            else:
                flash('Please provide both username and password', 'error')
        finally:
            cursor.close()
    return render_template('pages/login.html')

@auth_bp.route("/register", methods=["GET", "POST"])
def register():
    if 'user_id' in session:
        return redirect('/')
    
    if request.method == "POST":
        cursor = db.cursor(dictionary=True)
        try:
            userName = request.form.get("userName")
            emailId = request.form.get("emailId")
            password = request.form.get("password")
            
            if userName and emailId and password:
                cursor.execute("SELECT id FROM users WHERE user_name = %s OR email_id = %s", 
                             (userName, emailId))
                existing_user = cursor.fetchone()
                
                if existing_user:
                    flash('Username or email already exists', 'error')
                    return redirect('/register')
                
                cursor.execute(
                    "INSERT INTO users (user_name, email_id, password) VALUES (%s, %s, %s)",
                    (userName, emailId, password)
                )
                db.commit()
                flash('Registration successful! Please log in.', 'success')
                return redirect('/login')
            else:
                flash('Please fill in all fields', 'error')
        except Exception as e:
            db.rollback()
            flash(f'Registration failed: {str(e)}', 'error')
            print(f"Registration error: {e}")
        finally:
            cursor.close()
    
    return render_template('pages/register.html')

@auth_bp.route("/logout", methods=["POST"])
def logout():
    user_id = session.pop("user_id", None)
    user_name = session.pop("user_name", None)
    
    session.clear() 
    session.modified = True

    response = redirect('/')
    response.set_cookie('session', '', expires=0)
    return response

@auth_bp.route("/profile")
@login_required
def profile():
    cursor = db.cursor(dictionary=True)
    try:
        cursor.execute("SELECT user_name, email_id FROM users WHERE id = %s", 
                      (session.get('user_id'),))
        user = cursor.fetchone()
        return render_template('pages/profile.html', user=user)
    finally:
        cursor.close()