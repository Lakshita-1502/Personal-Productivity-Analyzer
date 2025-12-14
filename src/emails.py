import os
import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.mime.base import MIMEBase
from email import encoders

class Emails:
    def __init__(self, taskObj, valuePointObj):
        self.emailId=os.getenv("EMAILID")
        self.emailPassword=os.getenv("EMAILPASSWORD")
        self.taskDict=taskObj.taskDict
        self.valuePointDict=valuePointObj.valuePointDict

    def sendEmail(self):
        msg=MIMEMultipart("alternative")
        msg["Subject"]="Daily Productivity Report"
        msg["from"]=self.emailId
        msg["to"]=self.emailId
        html=self.generateMessage()
        msg.attach(MIMEText(html, "html", "utf-8")) 

        with open("./report.pdf", "rb") as f:
            part = MIMEBase("application", "octet-stream")
            part.set_payload(f.read())
        encoders.encode_base64(part)
        filename = os.path.basename("./report.pdf")
        part.add_header(
            "Content-Disposition",
            f'attachment; filename="{filename}"'
        )
        msg.attach(part)

        s=smtplib.SMTP('smtp.gmail.com', 587)
        s.starttls()
        s.login(self.emailId, self.emailPassword)
        s.send_message(msg)
        s.quit()
        print("Email send successfully")

    def generateMessage(self):
        taskDetails="""
        <body style="font-family: Arial; 
                    font-size: 10px; line-height: 1.2; color: #333333">
        <h3>Your Today's Productivity Analysis is given below:- </h3>
        <p>Today's Total Value Points are:- {self.totalValuePoints}</p>
        <p>Today's Total Completed Value Points are:- {self.totalCompletedValuePoints}</p>
        <p>Today's Total Pending Value Points are:- {self.totalPendingValuePoints}</p>
        <p>Today's Productivity Ratio:- {self.productivity}%</p>
        <p>For further details pls refer to the attached pdf. Thank You!</p>
        <p>You're receiving this system generate today's Summary.<br>© 2025 Personal Productivity Analyzer</p></body>"""
        return taskDetails
            
