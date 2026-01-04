from flask import Flask, session
from components.auth.routes import auth_bp
from components.tasks.routes import tasks_bp
from components.emailer.routes import email_bp
from datetime import timedelta

def create_app():
    app = Flask(__name__)
    
    # CRITICAL: Proper secret key
    app.secret_key = "your-secret-key-change-this-in-production-12345"
    
    # Session configuration
    app.config['PERMANENT_SESSION_LIFETIME'] = timedelta(days=7)
    app.config['SESSION_COOKIE_NAME'] = 'lockedin_session'
    app.config['SESSION_COOKIE_HTTPONLY'] = True
    app.config['SESSION_COOKIE_SAMESITE'] = 'Lax'
    
    # Register blueprints WITHOUT url_prefix
    app.register_blueprint(auth_bp)
    app.register_blueprint(tasks_bp)
    app.register_blueprint(email_bp)

    return app

app = create_app()

if __name__ == "__main__":
    app.run(debug=True, host='127.0.0.1', port=5000)