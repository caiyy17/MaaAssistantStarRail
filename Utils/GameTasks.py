import time
from .Controls import Controls
from .params import *


class GameTasks:
    def __init__(self, controls):
        self.controls = controls

    def backToMain(self):
        print("Back to main")
        while 1:
            if self.controls.find(dict["back"]):
                self.controls.tap(dict["back"])
            elif self.controls.find(dict["back2"]):
                self.controls.tap(dict["back2"])
            else:
                break
        self.controls.waitAndFind(dict["task"])

    def start(self):
        if (not self.controls.find(dict["task"])
                and not self.controls.quikFind(dict["back"])
                and not self.controls.quikFind(dict["back2"])):
            print("Start the game")
            self.controls.waitAndFindAndTap(dict["start"])
            self.controls.waitAndFind(dict["task"])
            print("Game started")
            return True
        else:
            self.backToMain()
            print("Game already started")
            return False

    def doTask(self, catergory, index, repeat=100):
        print(f"Do task {catergory} {index}")
        # Tepeport to the task location
        self.controls.tap(dict["task"])
        self.controls.findAndTap(dict["taskTab3"])
        self.controls.swipeAndFindAndTap(posDict["leftStart"],
                                         posDict["leftEnd"], dict[catergory])
        self.controls.swipeAndFind(posDict["rightStart"], posDict["rightEnd"],
                                   dict[index])
        self.controls.findRelativeAndTap(dict["taskTeleport"], dict[index],
                                         posDict["taskOffset"])
        # Find a way to start the task
        if (catergory == "taskSub2" or catergory == "taskSub3"
                or catergory == "taskSub4" or catergory == "taskSub5"
                or catergory == "taskSub6"):
            self.controls.waitAndFindAndTap(dict["battle"])
            if (catergory == "taskSub6"):
                if (self.controls.find(dict["battlePointZero"])):
                    self.controls.tap(dict["cancel"])
                    print("No battle point")
                    return
            if (self.controls.find(dict["powerRecharge"])):
                self.controls.tap(dict["cancel"])
                print("Power recharge")
                return
            self.controls.tap(dict["battleStart"])
            # sub4 need attack to start
            if (catergory == "taskSub4"):
                time.sleep(3)
                self.controls.swipePos(posDict["up"], posDict["up"], 1200)
                self.controls.tapPos(posDict["attack"])
            self.controls.waitAndFindAndTap(dict["auto"])
            repeat -= 1

            #battle loop
            while (repeat > 0):
                time.sleep(5)
                if (self.controls.waitAndFindAndTap(dict["battleAgain"], 100,
                                                    5)):
                    if catergory == "taskSub6":
                        if (self.controls.find(dict["battlePointZero"])):
                            self.controls.tap(dict["cancel"])
                            print("No battle point")
                            return
                    if (self.controls.find(dict["powerRecharge"])):
                        self.controls.tap(dict["cancel"])
                        self.controls.tap(dict["battleExit"])
                        print("Power recharge")
                        return
                repeat -= 1
            self.controls.waitAndFindAndTap(dict["battleExit"], 100, 5)
        elif catergory == "taskSub1":
            print("Not implemented")
            if (not self.controls.find(dict["task"])):
                self.controls.waitAndFind(dict["back2"])
        elif catergory == "taskSub7":
            print("Not implemented")
            if (not self.controls.find(dict["task"])):
                self.controls.waitAndFind(dict["back"])
        else:
            print("Task not found")