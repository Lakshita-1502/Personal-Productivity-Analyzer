class ValuePoints:
    def __init__(self, taskObj):
        self.taskDict=taskObj.taskDict
        self.valuePointDict={}

    def calculations(self):
        totalValuePoints=0
        totalCompletedValuePoints=0
        for value in self.taskDict.values():
            totalValuePoints+=value["valuePoints"]
            if value["pendingCompleted"]=="yes":
                totalCompletedValuePoints+=value["valuePoints"]
        totalPendingValuePoints=totalValuePoints-totalCompletedValuePoints
        productivity=round((totalCompletedValuePoints/totalValuePoints)*100, 2)
        self.valuePointDict["totalValuePoints"]=totalValuePoints
        self.valuePointDict["totalCompletedValuePoints"]=totalCompletedValuePoints
        self.valuePointDict["totalPendingValuePoints"]=totalPendingValuePoints
        self.valuePointDict["productivity"]=productivity
        self.displayCalc()

    def displayCalc(self):
        print(f"Total Value Points for the day:- {self.valuePointDict["totalValuePoints"]}")
        print(f"Total Value Points of completed tasks for the day:- {self.valuePointDict["totalCompletedValuePoints"]}")
        print(f"Productivity percentage:- {self.valuePointDict["productivity"]}%")
    
    