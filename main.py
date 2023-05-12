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


def main():
    controls = Controls(ADB,
                        ADBADRESS,
                        SCREEN,
                        device=navigationEvent["device"],
                        pressSteps=navigationEvent["pressSteps"],
                        releaseSteps=navigationEvent["releaseSteps"],
                        sendEventSize=navigationEvent["sendEventSize"])
    controls.connectADB()
    task = GameTasks(controls)
    map = MapNavigation(controls, posDict["mapOffset"], debugMode=True)

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
    route = [(255, 457), (253, 423), (254, 378), (260, 347), (264, 311),
             (264, 275), (268, 254), (300, 249), (337, 250), (369, 251),
             (374, 277), (375, 313), (376, 350), (377, 396), (378, 427),
             (373, 440), (347, 443), (314, 442), (288, 442), (269, 442),
             (261, 455)]
    map.setRoute(route, posDict["center"], posDict["rad"])
    while (1):
        te = time.time()
        print(te - ts)
        ts = te
        map.update()
        if (map.goRoute()):
            break


main()