import sys as sys
import os

sys.path.append(".")
from Utils.Controls import Controls

name = "screen0"

ADBADRESS = "127.0.0.1:5555"
ADB = "\"C:\Program Files\BlueStacks_nxt\.\HD-Adb.exe\""
dst = "./MakeMap/screen"
SCREEN = f"./MakeMap/screen/{name}.png"

if name == "screen0":
    #delete ild file
    for filename in os.listdir(dst):
        if not filename.endswith(".png"):
            continue
        else:
            # delete old files
            os.remove(dst + "/" + filename)

controls = Controls(ADB, ADBADRESS, SCREEN)
controls.connectADB()
controls.getScreen()