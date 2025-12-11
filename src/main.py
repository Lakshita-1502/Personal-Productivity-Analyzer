taskDict={}
count=1
more="y"
ans="y"

while (ans=="y"):
    more="y"
    print("Personal Productivity Manager\n")
    print("""Following are the choices offered by us:- 
        1. Add Task
        2. Update Task
        3. Delete Task
        4. Display all the Task""")
    choice=int(input("\nEnter the choice number:- "))

    while (more=="y"):
        if (choice==1):
            taskId=count
            taskName=input("Enter you task:- ")
            valuePoints=int(input(f"Enter value points (1-5) to Task {taskId}:- "))
            pendingCompleted=0
            taskArray=[taskName, valuePoints, pendingCompleted]
            taskDict[taskId]=taskArray
            count+=1
            more=input("Want to add more tasks? (y/n):- ")
        elif (choice==3):
            taskId=int(input("Enter task ID you want to delete:- "))
            del taskDict[taskId]
            more=input("Want to delete more tasks? (y/n):- ")
        elif (choice==4):
            for key, value in taskDict.items():
                print(f"Task ID:- {key}\nTask Description:- {value[0]}\nValue Points:- {value[1]}\nIs Completed:- {value[2]}")
            more="n"
            ans=input("Want to contnue? (y/n):- ")


