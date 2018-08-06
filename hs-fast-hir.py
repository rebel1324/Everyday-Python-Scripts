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

CURRENT_PATH = os.path.dirname(os.path.realpath(__file__))
TARGET_PATH_STUDIO = os.path.join(CURRENT_PATH, "hirfiles")
TARGET_PATH_NEO = os.path.join(CURRENT_PATH, "abdata", "studioneo", "HoneyselectItemResolver")
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
#ORDER_BY = input("")
ORDER_BY = "index"

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
            })

neoData = []
for fileData in targetFiles:
    filePath = fileData["path"]
    f = open(filePath, 'rt', encoding='UTF8')
    while (True):
        line = f.readline()
        if (not line): break
        line = cRegexComment.sub("", line)
        dataContent = cRegexData.findall(line)
        dataLength = len(dataContent)

        dataReference = {}
        if (dataLength > len(KEYNAME_LEGACY) + 1):
            dataReference = KEYNAMES.get(TYPE_NEO)
        else:
            dataReference = KEYNAMES.get(TYPE_STUDIO)

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

finalContent = finalContent + "<管理番号>"
finalContent = finalContent + "<種類番号>"
finalContent = finalContent + "<名称>"
finalContent = finalContent + "<マニフェスト>"
finalContent = finalContent + "<バンドルパス>"
finalContent = finalContent + "<ファイルパス>"
finalContent = finalContent + "<子の接続先>"
finalContent = finalContent + "<アニメがあるか>"
finalContent = finalContent + "<色替え>"
finalContent = finalContent + "<色替え対象>"
finalContent = finalContent + "<色替え(カラー２)>"
finalContent = finalContent + "<色替え対象(カラー２)>"
finalContent = finalContent + "<拡縮判定>"
finalContent = finalContent + "\n"

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
f = open(os.path.join(TARGET_PATH_NEO, TARGET_FILE_NAME), 'w', encoding='UTF8')
f.write(finalContent)
f.close()

MONO_FILE_NAME = "ItemList_00_00.MonoBehaviour"
CAT_FILE_NAME = "ItemGroup_00.MonoBehaviour"
PATH_TOOL_LISTPATH = os.path.join(CURRENT_PATH, "abdata", "studioneo", "info", "00.unity3d")
PATH_TOOL_MONOPATH = os.path.join(CURRENT_PATH, MONO_FILE_NAME)
PATH_TOOL_CATPATH = os.path.join(CURRENT_PATH, CAT_FILE_NAME)
SCRIPT_FILE_NAME = "exec.txt"

f = open(os.path.join(CURRENT_PATH, MONO_FILE_NAME), 'w', encoding='UTF8')
f.write(finalContent)
f.close()

categoryContent = "<種類番号><名称>\n"
categoryList = {
    "0": "일반 조형",
    "1": "베이스",
    "2": "가구",
    "3": "오브젝트",
    "4": "식품",
    "5": "무기",
    "6": "소형물체",
    "7": "캐릭터",
    "8": "H 아이템",
    "9": "액체",
    "10": "2D 효과",
    "11": "FX",
    "12": "기믹",
    "13": "3DSE",
    "14": "커스텀 분류",
    "15": "커스텀 분류",
    "16": "커스텀 분류",
    "17": "커스텀 분류",
    "18": "커스텀 분류",
    "19": "커스텀 분류",
    "20": "커스텀 분류",
    "21": "커스텀 분류",
    "22": "커스텀 분류",
    "23": "커스텀 분류",
    "24": "커스텀 분류",
    "25": "커스텀 분류",
    "26": "커스텀 분류",
    "27": "커스텀 분류",
    "28": "커스텀 분류",
    "29": "커스텀 분류",
    "70": "커스텀 분류",
    "71": "커스텀 분류",
    "72": "커스텀 분류",
    "73": "커스텀 분류",
    "74": "커스텀 분류",
    "75": "커스텀 분류",
    "76": "커스텀 분류",
    "77": "커스텀 분류",
    "78": "커스텀 분류",
    "79": "커스텀 분류",
}
for index, value in categoryList.items():
    categoryContent = categoryContent + "<" + index + ">"
    categoryContent = categoryContent + "<" + value + ">"
    categoryContent = categoryContent + "\n"

f = open(os.path.join(CURRENT_PATH, CAT_FILE_NAME), 'w', encoding='UTF8')
f.write(categoryContent)
f.close()

newScript = """
LoadPlugin(PluginDirectory+"UnityPlugin.dll")
unityParser0 = OpenUnity3d(path = "%s")
unityEditor0 = Unity3dEditor(parser = unityParser0)
unityEditor0.GetAssetNames(filter = True)
unityEditor0.ReplaceMonoBehaviour(path = "%s")
unityEditor0.GetAssetNames(filter = True)
unityEditor0.ReplaceMonoBehaviour(path = "%s")
unityEditor0.GetAssetNames(filter = True)
unityEditor0.SaveUnity3d(keepBackup = False, backupExtension = "._unity3d", background = False, pathIDsMode = -1)     
""" % (PATH_TOOL_LISTPATH, PATH_TOOL_MONOPATH, PATH_TOOL_CATPATH)

f = open(os.path.join(CURRENT_PATH, SCRIPT_FILE_NAME), 'w', encoding='UTF8')
f.write(newScript)
f.close()

PATH_UTIL = "D:\\hs\\rsvdir\\SB3UGS_v1.0.54delta\\SB3UtilityScript.exe"
os.system(PATH_UTIL + " " + os.path.join(CURRENT_PATH, SCRIPT_FILE_NAME))
