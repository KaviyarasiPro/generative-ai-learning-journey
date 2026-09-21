#project 2 - To Do List
tasks = []

while True:
    print("\n--- TO_DO LIST")
    print("1. Add Task")
    print("2. List Task")
    print("3. Remove Task")
    print("4. Exit")

    choice =input("Enter your Choice (1-4) :")

    if choice == "1":
      task = input("Enter a task : ")
      tasks.append(task)
      print("Task Addes sucessfully")

    elif choice == "2":
        if len(tasks) == 0:
            print("No tasks available.")
        else:
            print("\n your list Tasks:")
            for i,task in enumerate(tasks,start=1):
              print(i,".",task)

    elif choice == "3":
       if len(tasks) == 0:
           print("list is empty")
       else:
        print("\n your list Tasks:")
        for i,task in enumerate(tasks,start=1):
              print(i,".",task)
              
        number = int(input("\nEnter the List number to remove :"))

        if 1 <= number <= len(tasks):
            removed_task = tasks.pop(number-1)
            print(removed_task,"removed sucessfully")

        else:
            print("Invalid Task number")

    elif choice == "4":
        print("Thanks for using To-do List")
        break
    
    else:
        print("Invalid choice. please enter (1-4).")






        

    
