from tasks import Tasks
from valuePoints import ValuePoints
from graphs import Graphs

task=Tasks()
task.choices()

valuePoint=ValuePoints(task)
valuePoint.calculations()

graph=Graphs(valuePoint)
graph.plotGraph()