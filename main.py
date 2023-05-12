# init
import time
from Utils.Controls import Controls
from Utils.GameTasks import GameTasks
from Utils.MapNavigation import MapNavigation
from Utils.params import *
import multiprocessing

ADBADRESS = "127.0.0.1:5555"
ADB = "\"C:\Program Files\BlueStacks_nxt\.\HD-Adb.exe\""
SCREEN = "Screen/screen.png"

# init
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


def start():
    task.start()


def doTask(TaskName, TaskIndex):
    task.backToMain()
    task.doTask(TaskName, TaskIndex)
    task.backToMain()


def navigate():
    ts = time.time()
    map.setBigMap(dict["map21"])
    map.getInitPos()
    # route = [(255, 457), (253, 423), (254, 378), (260, 347), (264, 311),
    #          (264, 275), (268, 254), (300, 249), (337, 250), (369, 251),
    #          (374, 277), (375, 313), (376, 350), (377, 396), (378, 427),
    #          (373, 440), (347, 443), (314, 442), (288, 442), (269, 442),
    #          (261, 455)]
    route = [(253, 486), (256, 451), (262, 446), (287, 444), (331, 445),
             (374, 445), (384, 450), (388, 458), (390, 476), (393, 495),
             (400, 500), (410, 503), (427, 520), (445, 528), (454, 529),
             (455, 524), (455, 519), (455, 514), (456, 509), (461, 510),
             (474, 509), (489, 507), (488, 497), (489, 484), (491, 476),
             (493, 470), (499, 469), (509, 470), (519, 469), (523, 472),
             (522, 479), (525, 486), (529, 487), (535, 488), (544, 488),
             (550, 486), (553, 484), (553, 482), (555, 478), (560, 475),
             (560, 471), (560, 468), (560, 465), (562, 465), (565, 464),
             (566, 461), (565, 458), (566, 455), (566, 452), (569, 450),
             (571, 447), (573, 444), (574, 441), (573, 438), (572, 434),
             (570, 432), (572, 428), (570, 424), (570, 419), (570, 414),
             (571, 408), (573, 406), (578, 404), (589, 402), (606, 403),
             (626, 401), (641, 395)]
    map.setRoute(route, posDict["center"], posDict["rad"])
    while (1):
        te = time.time()
        print(te - ts)
        ts = te
        map.update()
        if (map.goRoute()):
            break


def tryFunc(func, *args):
    try:
        exitProcess()
        process = multiprocessing.Process(target=func, args=args)
        process.daemon = True
        process.start()
    except Exception as e:
        print(e)


def exitProcess():
    print(multiprocessing.active_children())
    for p in multiprocessing.active_children():
        p.terminate()
    controls.release()
    controls.release()
    task.backToMain()


def tryStart():
    tryFunc(start)


def tryDoTask(TaskName, TaskIndex):
    tryFunc(doTask, TaskName, TaskIndex)


def tryNavigate():
    tryFunc(navigate)


# gui part using tkinter
import tkinter as tk
from tkinter import ttk
from tkinter import messagebox


def gui():
    window = tk.Tk()
    window.title("AutoGame")
    window.geometry("500x300")
    window.resizable(False, False)

    # tab control
    tabControl = ttk.Notebook(window)
    tab1 = ttk.Frame(tabControl)
    tabControl.add(tab1, text="Main")
    tabControl.pack(expand=1, fill="both")
    tab2 = ttk.Frame(tabControl)
    tabControl.add(tab2, text="Task")
    tabControl.pack(expand=1, fill="both")
    tab3 = ttk.Frame(tabControl)
    tabControl.add(tab3, text="Map")
    tabControl.pack(expand=1, fill="both")

    # tab1 main
    # start button
    startButton = tk.Button(tab1, text="Start", command=tryStart)
    startButton.place(x=100, y=50, width=100, height=50)
    # exit button
    exitButton = tk.Button(tab1, text="Terminate", command=exitProcess)
    exitButton.place(x=300, y=50, width=100, height=50)

    # tab2 task
    # add a place to input the task name
    taskName = tk.StringVar()
    taskName.set("taskSub5")
    taskNameEntry = tk.Entry(tab2, textvariable=taskName)
    taskNameEntry.place(x=100, y=50, width=100, height=50)
    # add a place to input the task index
    taskIndex = tk.StringVar()
    taskIndex.set("taskSub5d")
    taskIndexEntry = tk.Entry(tab2, textvariable=taskIndex)
    taskIndexEntry.place(x=300, y=50, width=100, height=50)
    # get the task name and index
    TaskName = taskName.get()
    TaskIndex = taskIndex.get()

    # set taskName and taskIndex
    def setTaskName():
        TaskName = taskName.get()
        TaskIndex = taskIndex.get()
        doTaskButton = tk.Button(
            tab2,
            text="DoTask",
            command=lambda: tryDoTask(TaskName, TaskIndex))
        doTaskButton.place(x=300, y=150, width=100, height=50)
        print(TaskName, TaskIndex)

    # setTaskName button
    setTaskNameButton = tk.Button(tab2,
                                  text="SetTaskName",
                                  command=setTaskName)
    setTaskNameButton.place(x=100, y=150, width=100, height=50)

    # doTask button
    doTaskButton = tk.Button(tab2,
                             text="DoTask",
                             command=lambda: tryDoTask(TaskName, TaskIndex))
    doTaskButton.place(x=300, y=150, width=100, height=50)

    # tab3 map
    # navigate button
    navigateButton = tk.Button(tab3, text="Navigate", command=tryNavigate)
    navigateButton.place(x=100, y=50, width=100, height=50)

    window.mainloop()


if __name__ == "__main__":
    gui()