import time
from .Controls import Controls
from .params import *


class GameTasks:
    def __init__(self, controls, dict):
        self.controls = controls
        self.dict = dict

    def backToMain(self):
        print("Back to main")
        while 1:
            if self.controls.find(self.dict["back"]):
                self.controls.tap(self.dict["back"])
            elif self.controls.find(self.dict["back2"]):
                self.controls.tap(self.dict["back2"])
            else:
                break
        self.controls.waitAndFind(self.dict["task"])

    def start(self):
        print(self.dict["task"])
        if (not self.controls.find(self.dict["task"])
                and not self.controls.quikFind(self.dict["back"])
                and not self.controls.quikFind(self.dict["back2"])):
            print("Start the game")
            self.controls.waitAndFindAndTap(self.dict["start"])
            self.controls.waitAndFind(self.dict["task"])
            print("Game started")
            return True
        else:
            self.backToMain()
            print("Game already started")
            return False

    def doTask(self, catergory, index, repeat=100):
        print(f"Do task {catergory} {index}")
        # Tepeport to the task location
        self.controls.tap(self.dict["task"])
        self.controls.findAndTap(self.dict["taskTab3"])
        self.controls.swipeAndFindAndTap(posDict["leftStart"],
                                         posDict["leftEnd"],
                                         self.dict[catergory])
        self.controls.swipeAndFind(posDict["rightStart"], posDict["rightEnd"],
                                   self.dict[index])
        self.controls.findRelativeAndTap(self.dict["taskTeleport"],
                                         self.dict[index],
                                         posDict["taskOffset"])
        # Find a way to start the task
        if (catergory == "taskSub2" or catergory == "taskSub3"
                or catergory == "taskSub4" or catergory == "taskSub5"
                or catergory == "taskSub6"):
            self.controls.waitAndFindAndTap(self.dict["battle"])
            if (catergory == "taskSub6"):
                if (self.controls.find(self.dict["battlePointZero"])):
                    self.controls.tap(self.dict["cancel"])
                    print("No battle point")
                    return
            if (self.controls.find(self.dict["powerRecharge"])):
                self.controls.tap(self.dict["cancel"])
                print("Power recharge")
                return
            self.controls.tap(self.dict["battleStart"])
            # sub4 need attack to start
            if (catergory == "taskSub4"):
                time.sleep(3)
                self.controls.swipePos(posDict["up"], posDict["up"], 1200)
                self.controls.tapPos(posDict["attack"])
            self.controls.waitAndFindAndTap(self.dict["auto"])
            repeat -= 1

            #battle loop
            while (repeat > 0):
                time.sleep(5)
                if (self.controls.waitAndFindAndTap(self.dict["battleAgain"],
                                                    100, 5)):
                    if catergory == "taskSub6":
                        if (self.controls.find(self.dict["battlePointZero"])):
                            self.controls.tap(self.dict["cancel"])
                            print("No battle point")
                            return
                    if (self.controls.find(self.dict["powerRecharge"])):
                        self.controls.tap(self.dict["cancel"])
                        self.controls.tap(self.dict["battleExit"])
                        print("Power recharge")
                        return
                repeat -= 1
            self.controls.waitAndFindAndTap(self.dict["battleExit"], 100, 5)
        elif catergory == "taskSub1":
            print("Not implemented")
            if (not self.controls.find(self.dict["task"])):
                self.controls.waitAndFind(self.dict["back2"])
        elif catergory == "taskSub7":
            print("Not implemented")
            if (not self.controls.find(self.dict["task"])):
                self.controls.waitAndFind(self.dict["back"])
        else:
            print("Task not found")