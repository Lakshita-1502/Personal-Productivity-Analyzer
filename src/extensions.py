import mysql.connector
from config import sqlPassword

db=mysql.connector.connect(
    host="localhost",
    user="root",
    password=sqlPassword,
    database="personal_productivity_analyzer"
)