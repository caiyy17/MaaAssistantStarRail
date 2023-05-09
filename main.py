# init
import time
from Utils.Controls import Controls
from Utils.GameTasks import GameTasks
from Utils.MapNavigation import MapNavigation
from Utils.params import *

ADBADRESS = "127.0.0.1:5555"
ADB = "\"C:\Program Files\BlueStacks_nxt\.\HD-Adb.exe\""
SCREEN = "Screen/screen.png"

controls = Controls(ADB, ADBADRESS, SCREEN)
controls.connectADB()
task = GameTasks(controls)
map = MapNavigation(controls, posDict["mapOffset"])

# from begining to the main screen
# if (not task.start()):
#     task.backToMain()

# task example
# task.backToMain()
# task.doTask("taskSub5", "taskSub5c")
# task.backToMain()
# task.doTask("taskSub7", "taskSub7a", 1)
# task.backToMain()

# map example
map.setBigMap(dict["map21"])
map.getInitPos()
while (1):
    map.update(debugMode=True)
