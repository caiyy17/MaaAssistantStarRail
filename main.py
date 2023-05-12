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


class MaaAssistant():
    def __init__(self, address, adb, screen):
        self.address = address
        self.adb = adb
        self.screen = screen
        self.controls = Controls(
            self.adb,
            self.address,
            self.screen,
            device=navigationEvent["device"],
            pressSteps=navigationEvent["pressSteps"],
            releaseSteps=navigationEvent["releaseSteps"],
            sendEventSize=navigationEvent["sendEventSize"])
        self.controls.connectADB()
        self.task = GameTasks(self.controls)
        self.map = MapNavigation(self.controls,
                                 posDict["mapOffset"],
                                 debugMode=True)

    def start(self):
        self.task.start()

    def doTask(self, TaskName, TaskIndex):
        self.task.backToMain()
        self.task.doTask(TaskName, TaskIndex)
        self.task.backToMain()

    def navigate(self, bigMap, route):
        # ts = time.time()
        self.map.setBigMap(dict[bigMap])
        self.map.getInitPos()
        self.map.setRoute(route, posDict["center"],
                          [posDict["rad"][0], posDict["rad"][1]])
        while (1):
            # te = time.time()
            # print(te - ts)
            # ts = te
            self.map.update()
            if (self.map.goRoute()):
                break

    def findLocation(self, bigMap, route):
        self.map.setBigMap(dict[bigMap])
        self.map.getInitPos()
        self.map.setRoute(route, posDict["center"],
                          [posDict["rad"][0], posDict["rad"][1]])
        while (1):
            self.map.update()

    def tryFunc(self, func, *args):
        try:
            self.exitProcess()
            process = multiprocessing.Process(target=func, args=args)
            process.daemon = True
            process.start()
        except Exception as e:
            print(e)

    def exitProcess(self):
        print(multiprocessing.active_children())
        for p in multiprocessing.active_children():
            p.terminate()
        self.controls.release()
        self.controls.release()
        self.task.backToMain()


# gui part using tkinter
import tkinter as tk
from tkinter import ttk
from tkinter import messagebox


class MaaGui():
    def __init__(self, assistant):
        self.assistant = assistant
        self.TaskName = "taskSub5"
        self.TaskIndex = "taskSub5d"
        self.MapName = "map21"
        self.RouteName = "route1"
        self.route = dictRoute[self.RouteName]

    # set taskName and taskIndex
    def setTaskName(self, taskName, taskIndex):
        self.TaskName = taskName.get()
        self.TaskIndex = taskIndex.get()
        print(self.TaskName, self.TaskIndex)

    # set MapName and RouteName
    def setMapAndRoute(self, mapName, routeName):
        self.MapName = mapName.get()
        self.RouteName = routeName.get()
        self.route = dictRoute[self.RouteName]
        print(self.MapName, self.RouteName)

    # set address
    def updateSettings(self, address, adb):
        Adress = address.get()
        Adb = adb.get()
        self.assistant = MaaAssistant(Adress, Adb, SCREEN)
        print(Adress)
        print(Adb)

    def gui(self):
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
        tab4 = ttk.Frame(tabControl)
        tabControl.add(tab4, text="Settings")
        tabControl.pack(expand=1, fill="both")

        # tab1 main
        # start button
        startButton = tk.Button(
            tab1,
            text="Start",
            command=lambda: self.assistant.tryFunc(self.assistant.start))
        startButton.place(x=100, y=50, width=100, height=50)
        # exit button
        exitButton = tk.Button(tab1,
                               text="Terminate",
                               command=lambda: self.assistant.exitProcess())
        exitButton.place(x=300, y=50, width=100, height=50)

        # tab2 task
        # add a place to input the task name
        taskName = tk.StringVar()
        taskName.set(self.TaskName)
        taskNameEntry = tk.Entry(tab2, textvariable=taskName)
        taskNameEntry.place(x=100, y=50, width=100, height=50)
        # add a place to input the task index
        taskIndex = tk.StringVar()
        taskIndex.set(self.TaskIndex)
        taskIndexEntry = tk.Entry(tab2, textvariable=taskIndex)
        taskIndexEntry.place(x=300, y=50, width=100, height=50)
        # setTaskName button
        setTaskNameButton = tk.Button(
            tab2,
            text="SetTaskName",
            command=lambda: self.setTaskName(taskName, taskIndex))
        setTaskNameButton.place(x=100, y=150, width=100, height=50)
        # doTask button
        doTaskButton = tk.Button(
            tab2,
            text="DoTask",
            command=lambda: self.assistant.tryFunc(self.assistant.doTask, self.
                                                   TaskName, self.TaskIndex))
        doTaskButton.place(x=300, y=150, width=100, height=50)

        # tab3 map
        # add a place to input the map name
        mapName = tk.StringVar()
        mapName.set(self.MapName)
        mapNameEntry = tk.Entry(tab3, textvariable=mapName)
        mapNameEntry.place(x=100, y=50, width=100, height=50)
        # add a place to input the route
        routeName = tk.StringVar()
        routeName.set(self.RouteName)
        routeEntry = tk.Entry(tab3, textvariable=routeName)
        routeEntry.place(x=300, y=50, width=100, height=50)
        # setMapName button
        setMapNameButton = tk.Button(
            tab3,
            text="SetMapAndRoute",
            command=lambda: self.setMapAndRoute(mapName, routeName))
        setMapNameButton.place(x=100, y=150, width=100, height=50)
        # navigate button
        navigateButton = tk.Button(
            tab3,
            text="Navigate",
            command=lambda: self.assistant.tryFunc(self.assistant.navigate,
                                                   self.MapName, self.route))
        navigateButton.place(x=300, y=150, width=100, height=50)

        # tab4 setting
        # add a place to input the address
        address = tk.StringVar()
        address.set(self.assistant.address)
        addressEntry = tk.Entry(tab4, textvariable=address)
        addressEntry.place(x=100, y=50, width=300, height=50)
        # add a place to input the ADB
        adb = tk.StringVar()
        adb.set(self.assistant.adb)
        adbEntry = tk.Entry(tab4, textvariable=adb)
        adbEntry.place(x=100, y=100, width=300, height=50)
        # setAddress button
        setAddressButton = tk.Button(
            tab4,
            text="SetAddress",
            command=lambda: self.updateSettings(address, adb))
        setAddressButton.place(x=100, y=150, width=300, height=50)

        window.mainloop()


if __name__ == "__main__":
    assistant = MaaAssistant(ADBADRESS, ADB, SCREEN)
    gui = MaaGui(assistant)
    gui.gui()