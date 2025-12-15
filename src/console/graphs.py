import matplotlib.pyplot as plt
import numpy as np

class Graphs:
    def __init__(self, valuePointObj):
        self.valuePointDict=valuePointObj.valuePointDict

    def plotGraph(self):
        x=np.array([self.valuePointDict["totalCompletedValuePoints"], self.valuePointDict["totalPendingValuePoints"]])
        label=["Completed Value Points", "Pending Value Points"]
        plt.pie(x, labels=label)
        plt.title("Value Point distribution")
        plt.tight_layout()
        plt.savefig("graph.png")
        plt.show()
        plt.close()
