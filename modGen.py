#! python 3

from icalendar import Calendar
import os
import shutil

class Module():
    def __init__(self, modCode, modName):
        self.code = modCode
        self.name = modName
        self.lessons = []

def createYearDir(dirArr):
    yearNum = len(dirArr) + 1
    os.makedirs(f'Year {yearNum}', exist_ok=True)
    dirArr.append(f'Year {yearNum}')
    print(f'Made a Year {yearNum} Directory')

def createEmptySem(root):
    # Gets all the Year directories in root
    dirArr = sorted([i for i in os.listdir(root) if (os.path.isdir(i) and 'Year' in i)])
    print(dirArr)

    # If there are no year directories
    if not (dirArr):
        createYearDir(dirArr)

    for yrDir in dirArr:
        # Checks current year if semester directories exist
        semDir = os.listdir(yrDir)
        if len(semDir)< 2:
            newSemDir = os.path.join('.',yrDir,f'Sem {len(semDir)+1}')
            os.makedirs(newSemDir)
            print(f'Make module directories in {newSemDir}')
            return newSemDir

        # Both semester directories are in
        else:
            # Walks down the year directories and check if they are not empty
            for dirPath, dirNames, _ in sorted(os.walk(yrDir)):
                # If a semester directory is empty, setup module directories in there
                if 'Sem' in os.path.basename(dirPath) and not(dirNames):
                    print(f'Make module directories in {dirPath}')
                    return newSemDir
            else:
                # All semester directories have modules, create a new year directory
                createYearDir(dirArr)

# TODO: Probably change the input in future
FILE_PATH = 'nusmods_calendar.ics'
MOD_DICT = {}
ROOT_DIR = os.getcwd()


with open(FILE_PATH, 'rb') as calFile:
    cal = Calendar.from_ical(calFile.read())

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

targetSem = createEmptySem(ROOT_DIR)

# Creating the module directories
for key in MOD_DICT.keys():
    os.makedirs(os.path.join(targetSem,key))
    
# Creating the subdirectories for each module
for dirPath, dirNames, fileNames in os.walk(targetSem):
    mod = os.path.basename(dirPath)

    # Checks if the directory is the module
    if not(mod in MOD_DICT.keys()):
        continue
    
    # Creates a directory for each lesson type 
    [os.makedirs(os.path.join(dirPath, lesson)) for lesson in MOD_DICT[mod].lessons]


