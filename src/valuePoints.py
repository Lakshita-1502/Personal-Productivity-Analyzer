class ValuePoints:
    def __init__(self, taskObj):
        self.taskDict=taskObj.taskDict
        self.totalValuePoints=0
        self.totalCompletedValuePoints=0
        self.totalPendingValuePoints=0

    def calculations(self):
        for value in self.taskDict.values():
            self.totalValuePoints+=value["valuePoints"]
            if value["pendingCompleted"]=="yes":
                self.totalCompletedValuePoints+=value["valuePoints"]
        self.totalPendingValuePoints=self.totalValuePoints-self.totalCompletedValuePoints
        self.displayCalc()

    def displayCalc(self):
        print(f"Total Value Points for the day:- {self.totalValuePoints}")
        print(f"Total Value Points of completed tasks for the day:- {self.totalCompletedValuePoints}")
        productivity=round((self.totalCompletedValuePoints/self.totalValuePoints)*100, 2)
        print(f"Productivity percentage:- {productivity}%")
    
    