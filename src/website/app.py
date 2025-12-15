from flask import Flask, render_template, url_for

app=Flask(__name__)

@app.route('/')
def dashboard():
    return render_template('dashboard.html')

@app.route('/add-task', methods=['POST'])
def taskForm():     
    return render_template('taskForm.html')
if __name__=="__main__":
    app.run(debug=True)