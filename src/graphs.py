import matplotlib.pyplot as plt
import numpy as np

class Graphs:
    def __init__(self, valuePointObj):
        self.totalCompletedValuePoints=valuePointObj.totalCompletedValuePoints
        self.totalPendingValuePoints=valuePointObj.totalPendingValuePoints

    def plotGraph(self):
        self.x=np.array([self.totalCompletedValuePoints, self.totalPendingValuePoints])
        self.label=["Completed Value Points", "Pending Value Points"]
        plt.pie(self.x, labels=self.label)
        plt.show()