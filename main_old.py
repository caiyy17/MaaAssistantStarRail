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


def navigate(bigMap, route):
    # ts = time.time()
    map.setBigMap(dict[bigMap])
    map.getInitPos()
    map.setRoute(route, posDict["center"],
                 [posDict["rad"][0], posDict["rad"][1]])
    while (1):
        # te = time.time()
        # print(te - ts)
        # ts = te
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
    startButton = tk.Button(tab1, text="Start", command=lambda: tryFunc(start))
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
            command=lambda: tryFunc(doTask, TaskName, TaskIndex))
        doTaskButton.place(x=300, y=150, width=100, height=50)
        print(TaskName, TaskIndex)

    # setTaskName button
    setTaskNameButton = tk.Button(tab2,
                                  text="SetTaskName",
                                  command=setTaskName)
    setTaskNameButton.place(x=100, y=150, width=100, height=50)

    # doTask button
    doTaskButton = tk.Button(
        tab2,
        text="DoTask",
        command=lambda: tryFunc(doTask, TaskName, TaskIndex))
    doTaskButton.place(x=300, y=150, width=100, height=50)

    # tab3 map
    # add a place to input the map name
    mapName = tk.StringVar()
    mapName.set("map21")
    mapNameEntry = tk.Entry(tab3, textvariable=mapName)
    mapNameEntry.place(x=100, y=50, width=100, height=50)
    # add a place to input the route
    routeName = tk.StringVar()
    routeName.set("route1")
    routeEntry = tk.Entry(tab3, textvariable=routeName)
    routeEntry.place(x=300, y=50, width=100, height=50)
    # get the map name and route
    MapName = mapName.get()
    RouteName = routeName.get()
    route = dictRoute[RouteName]

    # set mapName
    def setMapAndRoute():
        MapName = mapName.get()
        RouteName = routeName.get()
        route = dictRoute[RouteName]
        navigateButton = tk.Button(
            tab3,
            text="Navigate",
            command=lambda: tryFunc(navigate, MapName, route))
        navigateButton.place(x=300, y=150, width=100, height=50)
        print(MapName, RouteName)

    # setMapName button
    setMapNameButton = tk.Button(tab3,
                                 text="SetMapAndRoute",
                                 command=setMapAndRoute)
    setMapNameButton.place(x=100, y=150, width=100, height=50)

    # navigate button
    navigateButton = tk.Button(
        tab3,
        text="Navigate",
        command=lambda: tryFunc(navigate, MapName, route))
    navigateButton.place(x=300, y=150, width=100, height=50)

    window.mainloop()


if __name__ == "__main__":
    gui()