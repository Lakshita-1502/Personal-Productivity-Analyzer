from dotenv import load_dotenv

from tasks import Tasks
from valuePoints import ValuePoints
from graphs import Graphs
from emails import Emails
from pdfs import Pdfs

load_dotenv()

task=Tasks()
task.choices()

valuePoint=ValuePoints(task)
valuePoint.calculations()

graph=Graphs(valuePoint)
graph.plotGraph()

email=Emails(task, valuePoint)
email.sendEmail()

pdf=Pdfs()
pdf.create_pdf()