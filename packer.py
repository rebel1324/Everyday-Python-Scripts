import re
import os
import zipfile
from os import path
from os import walk

PATH_CURRENT = os.getcwd();
PATH_HONEYSELECT = os.path.join("D:\hs")
PATH_ABDATA = os.path.join(PATH_HONEYSELECT, "abdata");
PATH_HIR_FOLDER = os.path.join(PATH_HONEYSELECT, "hirfiles");

PATH_HIR_PACKER_FOLDER = os.path.join(PATH_CURRENT, "mod");
PATH_DEFAULT_INCLUDES = os.path.join(PATH_CURRENT, "default");
PATH_RESULT = os.path.join(PATH_CURRENT, "result");


PATH_ZIP_HIR = "abdata/studioneo/HoneyselectItemResolver/"
PATH_ZIP_DIR = "abdata/"
PATH_ZIP_DIR_ROOT = "root/"
HIR_EXTENSION = ".txt"

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
REGEX_COMMENT = "(#.*\r*\n*)" #regex that eliminates the # comments
REGEX_DATACOL = "\<(.*?)\>" #regex that separates the data.
REGEX_NOBLANK = '[\r\n]+' #regex that eliminates the linefeed and linechanges.

# 작동 순서

# 요리 준비
# 1. 모드 팩커 HiR폴더 (PATH_HIR_PACKER_FOLDER)에 있는 HiR 파일들을 분석한다.
# 2. 분석한 파일을 기반으로 Mod class를 생성하고 생성한 Mod Class들을 Array에 다 처박아둔다.

# 요리 시작
# 1. 모드 팩커 파일을 Zip에 포함.
# 2. 디폴트 파일들을 Zip에 포함.
# 3. ABDATA에서 Mod Class에 포함된 unity3d 파일들을 Zip에 포함.

class Mod():
    def __init__(self, name):
        self.name = name; #모드의 이름
        self.listFiles = []; # 압축할 파일
        self.listUnityFiles = {}; #찾은 유니티 파일

    def setName(self, name):
        self.name = name;

    def addFile(self, file):
        self.listFiles.append(file);

    def addModFile(self, filename):
        self.listUnityFiles.update({
            filename: True
        });

modList = []
modDefaultList = []
cRegexComment = re.compile(REGEX_COMMENT)
cRegexData = re.compile(REGEX_DATACOL)
cRegexBlank = re.compile(REGEX_NOBLANK)

for (dirpath, dirnames, files) in walk(PATH_DEFAULT_INCLUDES):
    for filename in files:
        modDefaultList.append([os.path.join(dirpath, filename), filename])

for (dirpath, dirnames, files) in walk(PATH_HIR_PACKER_FOLDER):
    for filename in files:
        if (filename.find(HIR_EXTENSION) > 0):
            filePath = os.path.join(dirpath, filename)
            mod = Mod(filename.replace(HIR_EXTENSION, ""))
            mod.textFile = os.path.join(PATH_ZIP_HIR, filePath)

            f = open(filePath, 'rt', encoding='UTF8')
            while (True):
                line = f.readline()
                if (not line): break
                line = cRegexComment.sub("", line)
                dataContent = cRegexData.findall(line)
                dataLength = len(dataContent)
                dataReference = KEYNAME_NEO

                if (dataContent and dataLength > 0):
                    mod.addModFile(dataContent[4])
            f.close()

            for key in mod.listUnityFiles:
                mod.addFile(os.path.join(PATH_ZIP_DIR, key))

            modList.append(mod)

for mod in modList:
    newZip = zipfile.ZipFile(os.path.join(PATH_RESULT, mod.name + ".zip"), mode="w")

    newZip.write(mod.textFile, os.path.join(PATH_ZIP_DIR_ROOT, PATH_ZIP_HIR, mod.name + ".txt"))
    for file in mod.listFiles:
        newZip.write(os.path.join(PATH_HONEYSELECT, file), os.path.join(PATH_ZIP_DIR_ROOT, file))

    for file in modDefaultList:
        newZip.write(file[0], os.path.join(PATH_ZIP_DIR_ROOT, file[1]))
    print(newZip.namelist())
