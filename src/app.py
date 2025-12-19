from flask import Flask
from auth.routes import auth_bp
from tasks.routes import tasks_bp
from emailer.routes import email_bp

def create_app():
    app=Flask(__name__)
    app.register_blueprint(auth_bp)
    app.register_blueprint(tasks_bp)
    app.register_blueprint(email_bp)

    return app

app=create_app()

if __name__=="__main__":
    app.run(debug=True)