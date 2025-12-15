from flask import Flask, render_template, url_for, request

app=Flask(__name__)
tasks={}
taskId=1

@app.route('/', methods=['POST', 'GET'])
def taskForm():   
    global taskId
    if request.method=="POST":
        taskDesc=request.form.get("taskName")
        taskValue=request.form.get("valuePoint")
        if taskDesc:
            tasks[taskId]={"description": taskDesc, "valuePoints": taskValue}
            taskId+=1
    return render_template('taskForm.html',tasks=tasks)

if __name__=="__main__":
    app.run(debug=True)