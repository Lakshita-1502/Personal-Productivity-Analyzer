from flask import Flask, render_template, url_for, request, jsonify, redirect
import mysql.connector
import smtplib
from dotenv import load_dotenv
import os
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.mime.base import MIMEBase
from email.mime.image import MIMEImage
from email import encoders
import base64
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Image
from reportlab.lib.styles import getSampleStyleSheet
from reportlab.lib.pagesizes import A4

app=Flask(__name__)

load_dotenv()

sqlPassword=os.getenv("MYSQLPASSWORD")
emailId=os.getenv("EMAILID")
emailPassword=os.getenv("EMAILPASSWORD")

db=mysql.connector.connect(
    host="localhost",
    user="root",
    password=sqlPassword,
    database="personal_productivity_analyzer"
)

@app.route('/')
def home():
    return render_template("dashboard.html")

@app.route('/sign-up', methods=["POST","GET"])
def signUp():
    return render_template('signUp.html')

@app.route('/login', methods=["POST","GET"])
def login():
    return render_template('login.html')

@app.route('/add-task', methods=['POST', 'GET'])
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
    return render_template('taskForm.html', tasks=tasks)

@app.route('/update', methods=["POST"])
def update():
    cursor=db.cursor()
    data=request.get_json()
    cursor.execute("update tasks set completed=%s where id=%s", (data["completed"], data["id"]))
    db.commit()
    cursor.close()
    return jsonify(success=True)

@app.route('/delete/<int:task_id>', methods=["POST"])
def delete_task(task_id):
    cursor=db.cursor()
    cursor.execute("delete from tasks where id=%s", (task_id,))
    db.commit()
    cursor.close()
    return redirect('/add-task')

@app.route('/send-email', methods=["POST"])
def send_email():
    data=request.get_json()
    image_data=data["chart"].split(",")[1]
    image_bytes=base64.b64decode(image_data)

    with open("chart.png", "wb") as f:
        f.write(image_bytes)

    cursor=db.cursor(dictionary=True)
    cursor.execute("select name, value_points, completed from tasks")
    tasks=cursor.fetchall()
    cursor.close()

    total=sum(t["value_points"] for t in tasks)
    completed=sum(t["value_points"] for t in tasks if t["completed"])
    productivity=0 if total==0 else round((completed/total)*100, 2)

    pdf=SimpleDocTemplate("report.pdf", pagesize=A4)
    elements=[]
    styles=getSampleStyleSheet()

    elements.append(Paragraph(
        "<b>Daily Productivity Report</b>",
        styles["Title"]
    ))
    elements.append(Spacer(1,20))

    for t in tasks:
        elements.append(Paragraph(
            f"""<b>Task Name</b>:- {t["name"]}<br/>
            Value Points:- {t["value_points"]}<br/>""",
            styles["Normal"]
        ))
        elements.append(Spacer(1, 10))
    elements.append(Spacer(1, 20))

    elements.append(Paragraph(
        f"""
        <b>Total Points:</b> {total}<br/>
        <b>Completed Points:</b> {completed}<br/>
        <b>Productivity:</b> {productivity}%
        """,
        styles["Normal"]
    ))
    elements.append(Spacer(1, 20))

    elements.append(Image("chart.png", width=350, height=220))
    elements.append(Spacer(1, 20))

    elements.append(Paragraph(
        "© 2025 Personal Productivity Analyzer",
        styles["Normal"]
    ))
    elements.append(Spacer(1, 20))

    pdf.build(elements)

    msg=MIMEMultipart("alternative")
    msg["Subject"]="Productivity Report"
    msg["From"]=emailId
    msg["To"]=emailId

    html_body = f"""
        <body style="font-family: Arial; font-size: 12px; line-height: 1.2; color: #333333">
        <h3>Your Today's Productivity Analysis is given below:- </h3>
        <p>Today's Total Value Points are:- {total}</p>
        <p>Today's Total Completed Value Points are:- {completed}</p>
        <p>Today's Productivity Ratio:- {productivity}%</p>
        <p>You're receiving this system generate today's Summary.<br>© 2025 Personal Productivity Analyzer</p></body>"""
    
    msg.attach(MIMEText(html_body, "html", "utf-8"))

    with open("report.pdf", "rb") as f:
        part=MIMEBase("application","octet-stream")
        part.set_payload(f.read())
    encoders.encode_base64(part)
    filename=os.path.basename("report.pdf")
    part.add_header(
        "Content-Disposition",
        f'attachment; filename="{filename}"'
    )
    msg.attach(part)

    s=smtplib.SMTP('smtp.gmail.com', 587)
    s.starttls()
    s.login(emailId, emailPassword)
    s.send_message(msg)
    s.quit()
    return jsonify(success=True)

if __name__=="__main__":
    app.run(debug=True)