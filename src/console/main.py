from dotenv import load_dotenv
from console.tasks import Tasks
from console.valuePoints import ValuePoints
from console.graphs import Graphs
from console.emails import Emails
from console.pdfs import Pdfs

load_dotenv()

task=Tasks()
task.choices()

valuePoint=ValuePoints(task)
valuePoint.calculations()

graph=Graphs(valuePoint)
graph.plotGraph()

pdf=Pdfs(task)
pdf.create_pdf()

email=Emails(valuePoint)
email.sendEmail()
