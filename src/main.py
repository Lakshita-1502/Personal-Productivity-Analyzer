from dotenv import load_dotenv

from tasks import Tasks
from valuePoints import ValuePoints
from graphs import Graphs
from weather.fetchWeather import fetch_weather

load_dotenv()

task=Tasks()
task.choices()

valuePoint=ValuePoints(task)
valuePoint.calculations()

graph=Graphs(valuePoint)
graph.plotGraph()

weather=fetch_weather()
weather_data=weather.get_weather()
print(weather_data)