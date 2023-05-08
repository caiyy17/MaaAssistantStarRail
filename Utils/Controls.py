import subprocess
import time
from .FindOnScreen import findOnScreen


class Controls:
    def __init__(self, adb, adress, screen):
        self.adb = adb
        self.adress = adress
        self.screen = screen

    def connectADB(self):
        subprocess.run(f"{self.adb} connect {self.adress}",
                       capture_output=True,
                       shell=True)

    def getScreen(self):
        subprocess.run(
            f"{self.adb} -s {self.adress} shell screencap -p /sdcard/screen.png",
            capture_output=True,
            shell=True)
        subprocess.run(
            f"{self.adb} -s {self.adress} pull /sdcard/screen.png {self.screen}",
            capture_output=True,
            shell=True)

    def tapPos(self, pos, wait=1.5):
        subprocess.run(
            f"{self.adb} -s {self.adress} shell input tap {pos[0]} {pos[1]}",
            capture_output=True,
            shell=True)
        time.sleep(wait)

    def tap(self, target, wait=1.5):
        self.getScreen()
        x, y = findOnScreen(target, self.screen)
        if x == -1 or y == -1:
            raise Exception("Not found")
        self.tapPos([x, y], wait)

    def find(self, target):
        self.getScreen()
        x, y = findOnScreen(target, self.screen)
        if x == -1 or y == -1:
            return False
        return True

    def quikFind(self, target):
        x, y = findOnScreen(target, self.screen)
        if x == -1 or y == -1:
            return False
        return True

    def waitAndFind(self, target, timeout=100, interval=1):
        for i in range(timeout):
            if self.find(target):
                return True
            time.sleep(interval)
        raise Exception("Time out")

    def findAndTap(self, target, wait=1.5):
        if self.find(target):
            self.tap(target, wait)
            return True
        return False

    def waitAndFindAndTap(self, target, timeout=100, interval=1, wait=1.5):
        for i in range(timeout):
            if self.find(target):
                time.sleep(interval)
                self.tap(target, wait)
                return True
            time.sleep(interval)
        raise Exception("Time out")

    def swipePos(self, pos1, pos2, duration=2000):
        subprocess.run(
            f"{self.adb} -s {self.adress} shell input swipe {pos1[0]} {pos1[1]} {pos2[0]} {pos2[1]} {duration}",
            capture_output=True,
            shell=True)

    def swipe(self, target1, target2):
        self.getScreen()
        x1, y1 = findOnScreen(target1, self.screen)
        x2, y2 = findOnScreen(target2, self.screen)
        if x1 == -1 or y1 == -1 or x2 == -1 or y2 == -1:
            raise Exception("Not found")
        self.swipePos([x1, y1], [x2, y2])

    def swipeAndFind(self, pos1, pos2, target, timeout=10, interval=1):
        for i in range(timeout):
            if (not self.find(target)):
                self.swipePos(pos1, pos2)
                time.sleep(interval)
            else:
                return True
        raise Exception("Time out")

    def swipeAndFindAndTap(self,
                           pos1,
                           pos2,
                           target,
                           wait=1.5,
                           timeout=10,
                           interval=1):
        if (self.swipeAndFind(pos1, pos2, target, timeout, interval)):
            self.tap(target, wait)
            return True

    def findRelativeAndTap(self, target, pivot, offset, wait=1.5):
        self.getScreen()
        x, y = findOnScreen(pivot, self.screen)
        if x == -1 or y == -1:
            raise Exception("Pivot not found")
        x, y = findOnScreen(
            target,
            self.screen,
            roi=[x + offset[0], y + offset[1], offset[2], offset[3]])
        if x == -1 or y == -1:
            return False
        self.tapPos([x, y], wait)