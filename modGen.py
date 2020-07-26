#! python 3

from icalendar import Calendar
from mod import Module
import os
import shutil

# TODO: Probably change the input in future
FILE_PATH = 'nusmods_calendar.ics'
MOD_DICT = {}
ROOT_DIR = os.getcwd()

calFile = open(FILE_PATH, 'rb')

cal = Calendar.from_ical(calFile.read())

calFile.close()

# Gather the module information from the ical file
for comp in cal.walk():
    if comp.name == "VEVENT":
        # Returns [ Module Code, Lesson Type]
        summary = comp.get('summary').split(' ')

        # Returns [ Module Name, Tutorial Group]
        desc = comp.get('description').split('\n')

        modCode, modName, lessonType = summary[0], desc[0], ' '.join(summary[1:])
        
        # If the module is not registered yet
        if not(modCode in MOD_DICT.keys()):
            MOD_DICT[modCode] = Module(modCode, modName)

        # If the lesson is not registered yet
        if not(lessonType in MOD_DICT[modCode].lessons):
            MOD_DICT[modCode].lessons.append(lessonType)

# Creating the module directories
for key in MOD_DICT.keys():
    os.makedirs(key)
    
# Creating the subdirectories for each module
for dirPath, dirNames, fileNames in os.walk("."):
    mod = os.path.basename(dirPath)

    # Checks if the directory is the module
    if not(mod in MOD_DICT.keys()):
        continue

    # Creates the subdirectory for each module
    lessonPath = os.path.join(dirPath, lesson)
    
    # Creates a directory for each lesson type 
    [os.makedirs(lessonPath) for lesson in MOD_DICT[mod].lessons]

# ! FOR TESTING ONLY
# ! Deletes the directory & subdirectories after whole script has executed
for key in MOD_DICT.keys():
    shutil.rmtree(os.path.join('.',key))

