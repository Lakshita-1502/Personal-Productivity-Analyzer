import os
import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText

class Emails:
    def __init__(self, taskObj, valuePointObj):
        self.emailId=os.getenv("EMAIL_USER")
        self.emailPassword=os.getenv("EMAIL_PASSWORD")
        self.taskDict=taskObj.taskDict
        self.totalValuePoints=valuePointObj.totalValuePoints
        self.totalCompletedValuePoints=valuePointObj.totalCompletedValuePoints
        self.totalPendingValuePoints=valuePointObj.totalPendingValuePoints
        self.productivity=valuePointObj.productivity

    def sendEmail(self):
        msg=MIMEMultipart("alternative")
        msg["Subject"]="Daily Productivity Report"
        msg["from"]=self.emailId
        msg["to"]=self.emailId
        html=self.generateMessage()
        msg.attach(MIMEText(html, "html"))   

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
        <h2>Today's Task Details are as follows:- <h2>"""
        for key, value in self.taskDict.items():
            taskDetails+=f"""
            <b>Task ID:- {key} </b><br>
            <p>Task Description:- {value["taskName"]}</p>
            <p>Value Points:- {value["valuePoints"]}</p>
            <p>Completed:- {value["pendingCompleted"]}</p>"""
            
        taskDetails+=f"""
        <p>Today's Total Value Points are:- {self.totalValuePoints}</p>
        <p>Today's Total Completed Value Points are:- {self.totalCompletedValuePoints}</p>
        <p>Today's Total Pending Value Points are:- {self.totalPendingValuePoints}</p>
        <p>Today's Productivity Ratio:- {self.productivity}</p>"""
        taskDetails+="<p>You're receiving this system generate today's Summary.<br>© 2025 Personal Productivity Analyzer</p></body>"
        return taskDetails
            
