import json
import os
from collections import OrderedDict
from datetime import date

''' ******************** LOAD AND WRITE LOG ******************** '''

'''
Function: Load the file and return the contents of the file as JSON.
Expected: Contents will be return.
FileNotFoundError: The file is created with default data and contents will be returned. 
'''
def loadLog(filename):
    # Open the log
    try:
        # Potential LFI vuln
        with open("Logs/" + filename, "r") as json_file:
            contents = json.load(json_file)
    except FileNotFoundError:
        # print("File not accessible")
        # return "File doesn't exist"
        # Create the file
        contents = [{"Task":"Test","Category":"Test","Description":"Remove me!"}]
        writeLog(filename, contents)
    return contents

'''
Function: Write contents to log
Expected: Contents written to file
'''
def writeLog(filename, contents):
    # Check if directory exists
    if not os.path.isdir("./Logs/"):
        os.mkdir("./Logs/")

    # Potential LFI
    with open("Logs/" + filename, "w") as outfile:
        json.dump(contents, outfile, indent = 4)

''' ******************** VIEWING LOG ******************** '''

'''
Function: Read given dictionary and give tasks in viewable format from JSON.
Expected: Print out the log (without border).
'''
def displayLogContents(contents):
    # Print out the contents as Subject:Value
    index = 0
    for task in contents:
        firstSubject = True
        for subject,value in task.items():
            if firstSubject:
                indexString = str(index)
                print(f"[{indexString}] {subject}:{value}")
                firstSubject = False
            else:
                print(f"    {subject}:{value}")
        index += 1
        print()

'''
Function: Give task in viewable format from JSON
Expected: Print out specified task.
'''
def viewTask(task):
    for subject,value in task.items():
        print(f"{subject}:{value}")
    print()

''' ******************** EDITING LOG ******************** '''

'''
Function: Modifying Subjects
Expected: Returned the modified task with custom sorted subjects.
'''
def modifySubjects(taskDict, title):
    addingSubjects = True
    failedExit = False
    while addingSubjects:
        if failedExit:
            failMessage = "There must be a Task and Category subject and they must have values."
        else:
            failMessage = ""
        clearScreen()
        print(f'''**** {title} - SUBJECT ****
        
{failMessage}
''')
        
        viewTask(taskDict)        
        subject = input("Subject (Leave empty to exit): ")
        if not subject:
            # Before exiting
            # Check that task has a Task and Category Subject and that Task and Category subjects has values
            if False in [subject in taskDict for subject in ["Task","Category"]] or (not taskDict["Task"] and not taskDict["Category"]):
                failedExit = True
            else:
                # Conditions met to finish the task
                addingSubjects = False
        else:
            value = input(f"Value for {subject} (Leave empty to delete subject): ")
            if not value:
                if subject in taskDict:
                    del taskDict[subject]
                # If subject not in dict then don't create the subject
            else:
                taskDict[subject] = value
                failedExit = False
                
                # Sort dictionary so task is first and category is second.
                # Probably abit expensive after each edit but oh well :'(
                keyorder = ["Task","Category"]
                for subject in taskDict:
                    if subject not in ["Task","Category"]:
                        keyorder.append(subject)
                taskDict = OrderedDict(sorted(taskDict.items(), key=lambda i:keyorder.index(i[0])))
    
    return taskDict

''' ******************** HELPER FUNCTIONS ******************** '''

'''
Function: Ask for taskID and check validity
Expected: Returns a boolean value in relation to if taskID is valid or not
'''
def getTaskID(contents, title):
    # Ask for Task ID
    gettingTaskID = True
    failMessage = ""
    # Default just so the function has something to return in the case accessing loop fails.
    taskID = ""

    while gettingTaskID:
        failActive = False
        clearScreen()
        print(f'''**** {title} ****

{failMessage}
''')
        # Show logs to show 
        displayLogContents(contents)

        taskID = input("Task ID (Leave empty to quit): ")

        # We know taskID is a definitely a string here so we can use "not"
        if not taskID:
            break

        # Check if taskID is a number
        if not isNum(taskID):
            failMessage = "TaskID must be a positive number."
            failActive = True
        # Check if taskID is a valid index
        elif int(taskID) >= len(contents) or int(taskID) < 0:
            failMessage = "Please choose a valid index."
            failActive = True

        if not failActive:
            gettingTaskID = False
            taskID = int(taskID)
    return taskID


'''
Function: Check the validity of the date
Expected: Returns a boolean value in relation to if date is valid or not
'''
def checkValidDate(date):
    # Constraints
    # Day: 01-(Max day), Month: 01-12, Year: 1000-****

    dateParts = date.split("-")

    # Need three parts
    if(len(dateParts) != 3):
        return False

    day,month,year = date.split("-")
    try:
        day = int(day)
        month = int(month)
        year = int(year)
    except:
        return False

    # Get max day
    if(month==1 or month==3 or month==5 or month==7 or month==8 or month==10 or month==12):
        maxDay=31
    elif(month==4 or month==6 or month==9 or month==11):
        maxDay=30
    elif(year%4==0 and year%100!=0 or year%400==0):
        maxDay=29
    else:
        maxDay=28

    # All strings must be two characters (Two digits)
    index = 0
    for part in dateParts:
        if (index != 2 and len(part) != 2) or (index == 2 and len(part) != 4):
            # print("Day and month must have 2 digits and year must have 4 digits.")
            return False
        if not isNum(part):
            # print("Date must contain digits only.")
            return False
        index += 1

    if(month<1 or month>12):
        return False
    elif(day<1 or day>maxDay):
        return False

    return True

'''
Function: Clear the screen
Expected: Screen to be cleared
(Lul)
'''
def clearScreen():
    print("\033c")

def isNum(numString):
    if isinstance(numString, int) or numString == "0" or str.isdigit(numString):
        return True
    else:
        return False
