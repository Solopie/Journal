# Journal
> These notes are outdated so don't bother reading :'(

## Objective

Everyday there should be a outline of what tasks I have done.

## Data

- Should be in JSON format
- File name should be the date.
- Compulsory ( * )

( * ) Task: <Text>
( * ) Category: <Text>
Time Started: <Time>
Time Completed: <Time>
Time: <Time>
Difficulty: <Text>
Description: <Text>
Notes: <Text>
Size: <Text>

> Description and Notes are kinda the same.

> Size is use for food for now

## Add task Script (MyJournal.py)

Ability to add, modify or delete task for current or given date file.
Can add a task from the to-do list and remove task from to-do list.

### Functions

- Load file
    - Read the contents of file and return the data as JSON.
    - If file can't be found, then we create the file.

- Add task
- Modify task
- Remove task


## Statistics Script (showStats.py)

Display statistics on tasks throughout weeks, months or years.
Ability to display task count by category.


## Notes

- Task names are not unique and can be duplicated
- Subjects are unique in a task
- File should always exists as the file is create at the start of the script, however the file could be deleted whilst using the script. Therefore, if file isn't found then file is created.

