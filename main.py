# init
import time
from Utils.Controls import Controls
from Utils.GameTasks import GameTasks
from Utils.MapNavigation import MapNavigation
from Utils.params import *
import asyncio

ADBADRESS = "127.0.0.1:5555"
ADB = "\"C:\Program Files\BlueStacks_nxt\.\HD-Adb.exe\""
SCREEN = "Screen/screen.png"


async def main():
    controls = Controls(ADB,
                        ADBADRESS,
                        SCREEN,
                        device=navigationEvent["device"],
                        pressSteps=navigationEvent["pressSteps"],
                        releaseSteps=navigationEvent["releaseSteps"],
                        sendEventSize=navigationEvent["sendEventSize"])
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
    ts = time.time()
    map.setBigMap(dict["map21"])
    map.getInitPos()
    controls.pressAngle(posDict["center"], posDict["rad"][0])
    while (1):
        te = time.time()
        print(te - ts)
        ts = te
        map.update(debugMode=True)
        # map.update()
        controls.pressDeltaAngle(posDict["center"], posDict["rad"][0], 10)
    controls.release()


asyncio.run(main())