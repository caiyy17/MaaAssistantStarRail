import sys as sys
import os

sys.path.append(".")
from Utils.Controls import Controls

name = "screen0"

ADBADRESS = "127.0.0.1:5555"
ADB = "\"C:\Program Files\BlueStacks_nxt\.\HD-Adb.exe\""
dst = "./tools/MakeMap/screen"
SCREEN = f"./tools/MakeMap/screen/{name}.png"

if name == "screen0":
    #delete old files
    for filename in os.listdir(dst):
        if not filename.endswith(".png"):
            continue
        else:
            # delete old files
            os.remove(dst + "/" + filename)

controls = Controls(ADB, ADBADRESS, SCREEN)
controls.connectADB()
controls.getScreen()