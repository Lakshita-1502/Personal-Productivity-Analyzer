import matplotlib.pyplot as plt
import numpy as np

taskDict={}
totalTasks=1
moreTask="yes"
wantToContinue="yes"

#tasks CRUD operations
while (wantToContinue.lower()=="yes"):
    moreTask="yes"
    print("\nPersonal Productivity Manager\n")
    print("""Following are the choices offered by us:- 
        1. Add Task
        2. Update Task
        3. Delete Task
        4. Display Task""")
    choice=int(input("\nEnter the choice number:- "))

    while (moreTask.lower()=="yes"):
        if (choice==1):
            taskSubDict={}
            taskId=totalTasks
            taskName=input("\nEnter your task's description:- ")
            valuePoints=int(input(f"Enter value points (1-5) to Task {taskId}:- "))
            pendingCompleted="no"
            taskSubDict["taskName"]=taskName
            taskSubDict["valuePoints"]=valuePoints
            taskSubDict["pendingCompleted"]=pendingCompleted
            taskDict[taskId]=taskSubDict
            totalTasks+=1
            moreTask=input("Want to add more tasks:- ")

        elif (choice==2):
            taskId=int(input("\nEnter task ID you completed:- "))
            taskDict[taskId]["pendingCompleted"]="yes"
            moreTask=input("Any more task completed:- ")

        elif (choice==3):
            taskId=int(input("\nEnter task ID you want to delete:- "))
            del taskDict[taskId]
            moreTask=input("Want to delete more tasks:- ")

        elif (choice==4):
            for key, value in taskDict.items():
                print(f"\nTask ID:- {key}\n"+
                      f"Task Description:- {value["taskName"]}\n"
                      f"Value Points:- {value["valuePoints"]}\n"
                      f"Completed:- {value["pendingCompleted"]}")
            moreTask="no"
            wantToContinue=input("\nWant to continue:- ")

        else:
            print("Select a proper choice number")

#value point calculations
totalValuePoints=0
totalCompletedValuePoints=0
for value in taskDict.values():
    totalValuePoints+=value["valuePoints"]
    if value["pendingCompleted"]=="yes":
        totalCompletedValuePoints+=value["valuePoints"]
totalPendingValuePoints=totalValuePoints-totalCompletedValuePoints

print(f"Total Value Points for the day:- {totalValuePoints}")
print(f"Total Value Points of completed tasks for the day:- {totalCompletedValuePoints}")
productivity=round((totalCompletedValuePoints/totalValuePoints)*100, 2)
print(f"Productivity percentage:- {productivity}%")

#plotting graphs
#pie chart
x=np.array([totalCompletedValuePoints, totalPendingValuePoints])
label=["Completed Value Points", "Pending Value Points"]
plt.pie(x, labels=label)
plt.show()

#bar graph
x=np.array(["Completed Value Points", "Pending Value Points"])
y=np.array([totalCompletedValuePoints, (totalValuePoints-totalCompletedValuePoints)])
plt.bar(x, y)
plt.show()