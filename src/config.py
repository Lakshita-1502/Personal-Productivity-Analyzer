from dotenv import load_dotenv
import os

load_dotenv()

sqlPassword=os.getenv("MYSQLPASSWORD")
emailId=os.getenv("EMAILID")
emailPassword=os.getenv("EMAILPASSWORD")