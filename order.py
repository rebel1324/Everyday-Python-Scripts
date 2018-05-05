#
#   Match Anime Video and Subtitle Name Synced!
#   It works for the most of the time.
#   Syncing the subtitle based on the number.
#   The video file should follow regular file name format in the torrent site.
#
import re
import os
from os import path
from os import walk

print("ANIME SUBTITLE-VIDEO SYNCER")
print("I don't want to pay 15$ just for file sorter man")

print("========================================")

TARGET_PATH = os.path.dirname(os.path.realpath(__file__))
EPISODE_LENGTH = 2  # The episode has two digit number.
EXCLUDE_INFO = "(\((.*?)\))|(\[(.*?)\])"
EXTENTION = "(.\w)+$"
FIND_NUMBERS = '([0-9]{1,' + str(EPISODE_LENGTH) + '})'
SUBTITLE_NAME = ".smi"
WHITELIST = {".mkv": True, ".avi": True, ".mp4": True}

noinfo = re.compile(EXCLUDE_INFO)
epinum = re.compile(FIND_NUMBERS)
extnt = re.compile(EXTENTION)

forigin = []
for (dirpath, dirnames, filename) in walk(TARGET_PATH):
    forigin.extend(filename)
    break

index = 0
f = []
for name in forigin:
    f.insert(index, [noinfo.sub("", name.rsplit(".", 1)[0]), name])
    index = index + 1

episode = 0
index = 0
vidFiles = {}
subFiles = {}
isMatch = False
isSubtitle = False
maxEpisode = 10 ^ EPISODE_LENGTH - 1

while (episode <= maxEpisode):
    episode = episode + 1

    for data in f:
        filename = data[0]
        realname = data[1]

        result = epinum.findall(filename)
        isSubtitle = realname.find(SUBTITLE_NAME) > 0

        for foundNumber in result:
            isMatch = (int(foundNumber) == episode)
            if isMatch:
                if isSubtitle:
                    subFiles[episode] = realname
                else:
                    vidFiles[episode] = realname

                break

        isMatch = False
        isSubtitle = False

for index in vidFiles:
    filename = vidFiles[index]

    try:
        result = extnt.search(filename)
        if (WHITELIST[result[0]]):
            if subFiles[index]:
                repName = extnt.sub("", filename)
                os.rename(
                    path.join(TARGET_PATH, subFiles[index]),
                    path.join(TARGET_PATH, repName + SUBTITLE_NAME))

                print(subFiles[index] + " -> " + repName + SUBTITLE_NAME)
    except:
        pass

print("========================================")

os.system('pause')
