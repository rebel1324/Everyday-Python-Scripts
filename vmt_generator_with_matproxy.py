import re
import os
from os import path
from os import walk
import csv

#Core shits.
CSV_SKIN_PATH = "skinparams.csv"
CSV_TEX_PATH = "skintextures.csv"
ADDON_PATH = ""
MATERIAL_PATH = os.path.join(ADDON_PATH, "materials", "skin")

print("TFA SKIN VMT GENERATOR")
print("=======================================")
#Sorse Matproxies. They're just dick. since i don't want to write whole new parser
#I just made fixed vars inside of matproxies. thanks value fuck off please.
matProxyDefinitions = {
    "TextureOverlayScroll": [
        "{",
        "\toverlaycolor \"$color\"",
        "\tbrightoverlay \"$brightoverlay\"",
        "}"
    ]
}

#Open VMT CSVs
fileObject = open(CSV_SKIN_PATH, 'r', encoding='utf-8')
readerObject = csv.reader(fileObject)
fileTextureObject = open(CSV_TEX_PATH, 'r', encoding='utf-8')
readerTextureObject = csv.reader(fileTextureObject)

#Parse CSV Files in good data form so we can make files cunt.
#Parse original vmt data.
#textureGroup, textureName, parameter, value.
#with this combination we can support multiple models :DDD
parsedTextureCSV = {}
headerBool = False
for lineData in readerTextureObject:
    if (headerBool):
        #Register and parse Data.
        textureGroup = lineData[0]
        textureName = lineData[1]
        parameter = lineData[2]
        value = lineData[3]

        if not (textureGroup in parsedTextureCSV):
            parsedTextureCSV.update({textureGroup: {}})

        if not (textureName in parsedTextureCSV[textureGroup]):
            parsedTextureCSV[textureGroup].update({textureName: {}})

        parsedTextureCSV[textureGroup][textureName].update({parameter: value})
    else:
        #Skip header. just I don't want to think.
        headerBool = True

#Parse skin data so we can do something with it
parsedCSV = {}
headerBool = False
for lineData in readerObject:
    if (headerBool):
        #Register and parse Data.
        skinID = lineData[0]
        parameter = lineData[1]
        value = lineData[2]
        replaceIfExists = lineData[3]
        ignoreIfExists = lineData[4]

        if not (skinID in parsedCSV):
            parsedCSV.update({skinID: {}})

        parsedCSV[skinID].update({parameter: value})
    else:
        #Skip header. just I don't want to think.
        headerBool = True

#Close parse file object. your penis holds no power in here.
fileObject.close()
fileTextureObject.close()

#Start parsing.
for skinName, skinGroups in parsedTextureCSV.items():
    for skinGroup, parameters in skinGroups.items():
        for skinID, skinParameters in parsedCSV.items():
            vmtPath = os.path.join(MATERIAL_PATH, skinName, skinGroup, "{}.vmt".format(skinID))

            #create path.
            if not os.path.exists(os.path.dirname(vmtPath)):
                try:
                    os.makedirs(os.path.dirname(vmtPath))
                except OSError as exc:  # Guard against race condition
                    if exc.errno != errno.EEXIST:
                        raise

            #open file for write stream..
            f = open(vmtPath, 'w')
            f.write("\"VertexLitGeneric\"\n")
            f.write("{\n")

            mergedParameters = {}
            listOfProxy = []
            #Merge parameter values.
            for parameter, value in parameters.items():
                mergedParameters.update({parameter: value})
            for parameter, value in skinParameters.items():
                if (parameter == "proxy"):
                    listOfProxy.append(value)
                else:
                    mergedParameters.update({parameter: value})

            #Write merged parameters.
            for parameter, value in mergedParameters.items():
                f.write("\t\"{}\" \"{}\"\n".format(parameter, value))

            #Check if there is matproxy.
            if (len(listOfProxy) > 0):
                #write matproxy array.
                f.write("\tProxies\n")
                f.write("\t{\n")
                #add matproxy texts.
                for proxyName in listOfProxy:
                    if (matProxyDefinitions[proxyName]):
                        f.write("\t\t{}\n".format(proxyName))
                        for line in matProxyDefinitions[proxyName]:
                            f.write("\t\t{}\n".format(line))
                f.write("\t}\n")
            f.write("}\n")

            #close file and end write stream.
            f.close()

            #log them
            print("SAVED VMT: " + vmtPath)

print("=======================================")
