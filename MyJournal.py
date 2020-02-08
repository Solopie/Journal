import json
import os
from datetime import date

from LogFunctions import *

def main():
    # Check if input is valid date
    checkingDate = True
    failedExit = False
    failMessage = "Log: Nothing to report :)"
    while checkingDate:
        if failedExit:
            failMessage = "Log: The date given was invalid."
        clearScreen()
        print(f'''**** Welcome to the Journal Application! ****

{failMessage}

Date format: dd-mm-YYYY
E.g. 01-01-2020
''')
        inputDate = input("Please input date (Leave empty to use today's date): ")
        if not inputDate:
            break
        
        # End loop if valid date
        if checkValidDate(inputDate):
            checkingDate = False
        else:
            failedExit = True
    # Default date to current date or use inputDate if it's not empty
    filename = date.today().strftime("%d-%m-%Y")
    if inputDate:
        filename = inputDate

    mainMenuActive = True
    # Default log message
    logMessage = "Nothing to report :)"
    while mainMenuActive:
        clearScreen()
        print("**** MAIN MENU ****\n")
        # This is where the result string given by function will be outputted to
        print(f"Log: {logMessage}")
        
        # Show options
        askOptions = f'''
Date: {filename}

Options:
    1 - View tasks
    2 - Add task
    3 - Modify task
    4 - Delete task
    5 - Exit program

Please enter a number option: '''
        option = input(askOptions)
        resultFunction = chooseOption(option)
        
        # Keep asking for option until valid option is given
        if isinstance(resultFunction,str):
            logMessage = resultFunction
        else:
            logMessage = resultFunction(filename)
            if not logMessage:
                logMessage = "Nothing to report :)"
        
def chooseOption(option):
    if not option:
        return "Please enter a number."
    if not isNum(option):
        return "Please give a positive number."

    option = int(option)
    options = {
            1: displayLogFile,
            2: addTask,
            3: modifyTask,
            4: deleteTask,
    }

    if(option == 5):
        clearScreen()
        raise SystemExit

    return options.get(option, "Invalid Option")

'''
MAJOR FUNCTION
Function: Read file and give tasks in viewable format from JSON.
Expected: Print out the log. 
'''
def displayLogFile(filename):
    clearScreen()
    print("**** VIEW LOG ****\n")
    contents = loadLog(filename)
    displayLogContents(contents)
    print("******************\n")

    input("(PRESS ENTER TO EXIT)")

    return "Log has been viewed."

'''
MAJOR FUNCTION
Function: Add task to log
Expected: Log should be updated with new task
'''
def addTask(filename):
    clearScreen()
    print("****ADD TASK****\n\n\n")
    contents = loadLog(filename)
    taskName = input("Task: ")
    if not taskName:
        return "Add task has been cancelled."
    taskCategory = input("Category: ")
    while not taskCategory:
        clearScreen()
        print(f'''****ADD TASK****

Category must have a value.        

Task: {taskName}''')
        taskCategory = input("Category: ")
    taskDict = {"Task":taskName, "Category":taskCategory}

    # Modifying subjects
    taskDict = modifySubjects(taskDict, "ADD TASK")

    contents.append(taskDict)
    writeLog(filename, contents)

    return f"Task \"{taskName}\" added."

'''
MAJOR FUNCTION
Function: Choose a task to modify.
Expected: Task subjects and values modified.
'''
def modifyTask(filename):
    contents = loadLog(filename)
    isFirstModify = True

    if len(contents) == 0:
        return "No tasks to modify."

    modifyTaskActive = True
    while modifyTaskActive:
        taskID = getTaskID(contents, "MODIFY TASK")

        # If number is 0, value is false
        if not isNum(taskID) and not taskID:
            break
        
        # If taskID is valid then we have done a modify
        isFirstModify = False        

        # Task Dictionary
        taskDict = contents[taskID]

        # Modify the task subjects
        contents[taskID] = modifySubjects(taskDict, "MODIFY TASK")
    
    if isFirstModify:
        # Nothing was modified
        return "Modify Task has been cancelled."
    else:
        writeLog(filename, contents)
        return "Tasks has been modified."

'''
MAJOR FUNCTION
Function: Delete task
Expected: Log is modified
'''
def deleteTask(filename):
    contents = loadLog(filename)
    if len(contents) == 0:
        return "No tasks to delete."

    displayLogContents(contents)

    taskID = getTaskID(contents, "DELETE TASK")    

    # If number is 0, value is false
    if not isNum(taskID) and not taskID:
        return "Delete task cancelled."

    # Delete task
    del contents[taskID]
    writeLog(filename, contents)

    return "Task deleted."

if __name__ == "__main__":
    main()

