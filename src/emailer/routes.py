from flask import Blueprint, Flask, render_template, url_for, request, jsonify, redirect
from extensions import db
from config import emailId, emailPassword
import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.mime.base import MIMEBase
from email.mime.image import MIMEImage
from email import encoders
import base64
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Image
from reportlab.lib.styles import getSampleStyleSheet
from reportlab.lib.pagesizes import A4
import os

email_bp = Blueprint("email", __name__)

@email_bp.route("/send-email", methods=["POST"])
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
