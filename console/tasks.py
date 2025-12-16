class Tasks:
    def __init__(self):
        self.taskDict={}
        self.totalTasks=1
        self.moreTask="yes"
        self.wantToContinue="yes"

    def choices(self):
        while (self.wantToContinue.lower()=="yes"):
            self.moreTask="yes"
            self.displayChoices()
            choice=int(input("\nEnter the choice number:- "))

            while (self.moreTask.lower()=="yes"):
                if (choice==1):
                    self.addTask()

                elif (choice==2):
                    self.updateTask()

                elif (choice==3):
                    self.deleteTask()

                elif (choice==4):
                    self.displayTask()

                else:
                    print("Select a proper choice number")
                    self.moreTask="no"

    def displayChoices(self):
        print("\nPersonal Productivity Manager\n")
        print("""Following are the choices offered by us:- 
                1. Add Task
                2. Update Task
                3. Delete Task
                4. Display Task""")

    def addTask(self):
        taskSubDict={}
        taskId=self.totalTasks
        taskName=input("\nEnter your task's description:- ")
        valuePoints=int(input(f"Enter value points (1-5) to Task {taskId}:- "))
        pendingCompleted="no"
        taskSubDict["taskName"]=taskName
        taskSubDict["valuePoints"]=valuePoints
        taskSubDict["pendingCompleted"]=pendingCompleted
        self.taskDict[taskId]=taskSubDict
        self.totalTasks+=1
        self.moreTask=input("Want to add more tasks:- ")

    def updateTask(self):
        taskId=int(input("\nEnter task ID you completed:- "))
        self.taskDict[taskId]["pendingCompleted"]="yes"
        self.moreTask=input("Any more task completed:- ")

    def deleteTask(self):
        taskId=int(input("\nEnter task ID you want to delete:- "))
        del self.taskDict[taskId]
        self.moreTask=input("Want to delete more tasks:- ")

    def displayTask(self):
        for key, value in self.taskDict.items():
            print(f"\nTask ID:- {key}\n"+
                f"Task Description:- {value["taskName"]}\n"
                f"Value Points:- {value["valuePoints"]}\n"
                f"Completed:- {value["pendingCompleted"]}")
        self.moreTask="no"
        self.wantToContinue=input("\nWant to continue:- ")