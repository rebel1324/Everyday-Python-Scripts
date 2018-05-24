#
#   Sort out the text with certain rules
#   lmao this is that game that you heared about.
#   :(((
#
import re
import os
from os import path
from os import walk

print("STUDIO ITEM COMBINER AND SORTER - It does the job!")
print("================================================")

ORDER_BY = "name"

TARGET_PATH_STUDIO = os.path.dirname(os.path.realpath(__file__)) + "\\abdata\\studio\\itemobj\\honey\\HoneyselectItemResolver"
TARGET_PATH_NEO = os.path.dirname(os.path.realpath(__file__)) + "\\abdata\\studioneo\\HoneyselectItemResolver"
TARGET_PATH_TEST = os.path.dirname(os.path.realpath(__file__))
TARGET_FILE_NAME = "goodcunt.txt"

REGEX_COMMENT = "(#.*\r*\n*)" #regex that eliminates the # comments
REGEX_DATACOL = "\<(.*?)\>" #regex that separates the data.
REGEX_NOBLANK = '[\r\n]+' #regex that eliminates the linefeed and linechanges.
FILE_EXTENTION = '.txt'

TYPE_STUDIO = 0
TYPE_NEO = 1

KEYNAME_STABLE = {
    0: "index",  #Item Index.
    1: "package",  #Name of the item. (used in the UI)
    2: "name",  #Name of the item. (used in the UI)
}
KEYNAME_NEO = {
    0: "index",  #Item Index.
    1: "category",  #Category that item belongs.
    2: "name",  #Name of the item. (used in the UI)
    3: "manifest",  #undefined.
    4: "package",  #Path of the unity package. (used in the Internal Game Mechanism)
    5: "object",  #GameObject Name that system will spawn. 
    6: "child",  #undefined.
    7: "animated",  #boolean of whether item is animated or not.
    8: "colorable",  #boolen of whether item is colorable or not.
    9: "colorObject",  #GameObject that will affected by the color functions.
    10: "colorable2",  #boolen of whether item is colorable or not. (2nd Slot)
    11: "colorObject2",  #GameObject that will affected by the color functions. (2nd Slot)
    12: "hasFK",  #GameObject that will affected by the color functions. (2nd Slot)
}
KEYNAME_LEGACY = {
    0: "actual", #Actual Index of the studio item. unused.
    1: "comment", #Comment that is used internally. unused.
    2: "index", #Item Index.
    3: "category", #Category that item belongs.
    4: "name", #Name of the item. (used in the UI)
    5: "package", #Path of the unity package. (used in the Internal Game Mechanism)
    6: "object", #GameObject Name that system will spawn. 
}
KEYNAMES = {TYPE_STUDIO: KEYNAME_LEGACY, TYPE_NEO: KEYNAME_NEO}

print("List of sort type available:")
for key in KEYNAME_STABLE:
    print(KEYNAME_STABLE[key])
print("Enter any sort type you want to perform from above:")
ORDER_BY = input("")

notFound = True
for key in KEYNAME_STABLE:
    if (KEYNAME_STABLE[key] == ORDER_BY):
        notFound = False

if (notFound == True):
    print("ORDER NAME IS NOT VALID!")
    print("only following sort can be done:")
    for key in KEYNAME_STABLE:
        print(KEYNAME_STABLE[key])
    quit(0)

cRegexComment = re.compile(REGEX_COMMENT)
cRegexData = re.compile(REGEX_DATACOL)
cRegexBlank = re.compile(REGEX_NOBLANK)

targetFiles = []
for (dirpath, dirnames, files) in walk(TARGET_PATH_STUDIO):
    for filename in files:
        if (filename.find(FILE_EXTENTION) > 0):
            targetFiles.append({
                "path": os.path.join(dirpath, filename),
                "type": TYPE_STUDIO
            })

for (dirpath, dirnames, files) in walk(TARGET_PATH_NEO):
    for filename in files:
        if (filename.find(FILE_EXTENTION) > 0):
            targetFiles.append({
                "path": os.path.join(dirpath, filename),
                "type": TYPE_NEO
            })

neoData = []
for fileData in targetFiles:
    fileType = fileData["type"]
    filePath = fileData["path"]
    dataReference = KEYNAMES[fileType]
    if (dataReference):
        f = open(filePath, 'rt', encoding='UTF8')
        while (True):
            line = f.readline()
            if (not line): break
            line = cRegexComment.sub("", line)
            dataContent = cRegexData.findall(line)
            dataLength = len(dataContent)
            if (dataContent and dataLength > 0):
                newData = {}

                for index in range(0, dataLength):
                    keyName = dataReference.get(index)
                    if (keyName):
                        newData[keyName] = dataContent[index]

                neoData.append(newData)
        f.close()

print("Studio Item Parsing Finished!")
print("Total Item Counts: ", len(neoData))

from collections import OrderedDict

sortedIndex = {}
for index in range(0, len(neoData)):
    sortedIndex[index] = neoData[index].get(ORDER_BY)

sortedIndex = OrderedDict(sorted(sortedIndex.items(), key=lambda t: t[1]))

finalContent = ""
for index in sortedIndex:
    itemData = neoData[index]
    if (itemData):
        finalContent = finalContent + "<" + itemData.get("index", "") + ">"
        finalContent = finalContent + "<" + itemData.get("category", "0") + ">"
        finalContent = finalContent + "<" + itemData.get("name", "_ERROR_") + ">"
        finalContent = finalContent + "<" + itemData.get("manifest", "") + ">"
        finalContent = finalContent + "<" + itemData.get("package", "_ERROR_") + ">"
        finalContent = finalContent + "<" + itemData.get("object", "_ERROR_") + ">"
        finalContent = finalContent + "<" + itemData.get("child", "") + ">"
        finalContent = finalContent + "<" + itemData.get("animated", "false") + ">"
        finalContent = finalContent + "<" + itemData.get("colorable", "false") + ">"
        finalContent = finalContent + "<" + itemData.get("colorObject", "") + ">"
        finalContent = finalContent + "<" + itemData.get("colorable2", "false") + ">"
        finalContent = finalContent + "<" + itemData.get("colorObject2", "") + ">"
        finalContent = finalContent + "<" + itemData.get("hasFK", "false") + ">"
        finalContent = finalContent + "\n"

# writedata.py
f = open(os.path.join(TARGET_PATH_TEST, TARGET_FILE_NAME), 'w', encoding='UTF8')
f.write(finalContent)
f.close()

os.system('pause')