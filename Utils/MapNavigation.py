import math
import numpy as np
import cv2
from matplotlib import pyplot as plt
from .PatchMatch import *

std_width: int = 1280
std_height: int = 720
search_width: int = 130
search_height: int = 130
SMALL = 1
LARGE = 1.3
STEPS = 10

THRESHDIR = 0.8
THRESHUPDATE = 10
THRESHRUN = 50


class MapNavigation:
    def __init__(self, controls, roi, debugMode=False):
        self.roi = roi
        self.controls = controls
        self.screen = controls.screen
        self.debugMode = debugMode
        self.controls.getScreen()

    def setBigMap(self, bigMap):
        map = cv2.imread(bigMap)
        self.bigMap = getEdge(map)
        cv2.imwrite("Screen/bigMap.png", self.bigMap)
        self.index = 0
        self.source = cv2.imread(bigMap)
        if self.debugMode:
            self.debug = self.source.copy()

    def setRoute(self, route, controlCenter, controlRadius):
        self.route = np.array(route)
        self.routeIndex = 0
        self.routeLen = len(route)
        self.controlCenter = controlCenter
        self.controlRadius = controlRadius
        if self.debugMode:
            for i in range(self.routeLen):
                cv2.circle(self.debug,
                           (int(self.route[i][0]), int(self.route[i][1])), 4,
                           (0, 255, 0), -1)

    # find current position
    def getMap(self):
        self.controls.getScreen()
        screen_img = cv2.imread(self.screen)
        screen_img = cv2.resize(screen_img, (std_width, std_height),
                                interpolation=cv2.INTER_CUBIC)
        left = int(self.roi[0])
        top = int(self.roi[1])
        right = left + int(self.roi[2])
        bottom = top + int(self.roi[3])
        # if not (0,0,0,0), crop roi
        if bottom != 0:
            screen_img = screen_img[top:bottom, left:right]
        screen_img = getEdge(screen_img)
        # print(screen_img.shape)
        return screen_img

    def getInitPos(self):
        self.current = self.getMap()
        self.analyzeFull()

    def update(self):
        self.current = self.getMap()
        self.index += 1
        if not (self.analyze()):
            if self.debugMode:
                self.debug = self.source.copy()
            self.analyzeFull()
        if self.debugMode:
            cv2.circle(self.debug, (int(self.mapPos[0]), int(self.mapPos[1])),
                       4, (0, 0, 255), -1)
            cv2.imwrite(f"Screen/debug.jpg", self.debug)

    def analyze(self, threshold=50):
        img1 = self.current  # queryImage
        size = img1.shape
        mapOffset = [
            -self.offset[0] + (search_width - size[1]) / 2,
            -self.offset[1] + (search_height - size[0]) / 2,
        ]
        searchMap = cv2.warpAffine(
            self.bigMap,
            np.float32([[1, 0, mapOffset[0]], [0, 1, mapOffset[1]]]),
            (search_width, search_height))
        currentOffset, valueMax, currentScale = patchMatchScale(
            img1, SMALL, LARGE, STEPS, searchMap)
        if (abs(currentOffset[0]) > threshold
                or abs(currentOffset[1]) > threshold):
            return False
        self.offset = [
            -mapOffset[0] + currentOffset[0], -mapOffset[1] + currentOffset[1]
        ]
        self.mapPos = [
            self.offset[0] + self.current.shape[1] / 2,
            self.offset[1] + self.current.shape[0] / 2,
        ]
        # shift = [(1 - currentScale) * size[1] / 2,
        #          (1 - currentScale) * size[0] / 2]
        # final1 = cv2.warpAffine(
        #     img1,
        #     np.float32([[currentScale, 0, shift[0]],
        #                 [0, currentScale, shift[1]]]), (size[1], size[0]))
        # res = cv2.warpAffine(
        #     final1, np.float32([[1, 0, self.offset[0]], [0, 1,
        #                                                  self.offset[1]]]),
        #     (self.bigMap.shape[1], self.bigMap.shape[0]))
        # cv2.imwrite(f"Screen/align{self.index}.jpg", self.bigMap - res + 128)
        # print(valueMax, currentScale, self.offset)
        return True

    def analyzeFull(self):
        img1 = self.current  # queryImage
        size = img1.shape
        currentOffset, valueMax, currentScale = patchMatchScale(
            img1, SMALL, LARGE, STEPS, self.bigMap)
        self.offset = currentOffset
        self.mapPos = [
            self.offset[0] + self.current.shape[1] / 2,
            self.offset[1] + self.current.shape[0] / 2,
        ]
        # shift = [(1 - currentScale) * size[1] / 2,
        #          (1 - currentScale) * size[0] / 2]
        # final = cv2.warpAffine(
        #     img1,
        #     np.float32([[currentScale, 0, shift[0]],
        #                 [0, currentScale, shift[1]]]), (size[1], size[0]))
        # res = cv2.warpAffine(
        #     final,
        #     np.float32([[1, 0, self.offset[0]], [0, 1, self.offset[1]]]),
        #     (self.bigMap.shape[1], self.bigMap.shape[0]))
        # cv2.imwrite(f"Screen/align{self.index}.jpg", self.bigMap - res + 128)
        # print(valueMax, currentScale, self.offset)

    # navigation to target
    def updateTarget(self):
        while self.routeIndex < self.routeLen:
            direction = [
                self.route[self.routeIndex][0] - self.mapPos[0],
                self.route[self.routeIndex][1] - self.mapPos[1]
            ]
            if (direction[0]**2 + direction[1]**2) < THRESHUPDATE**2:
                self.routeIndex += 1
            else:
                break

    def move(self, direction, run=False):
        distance2 = direction[0]**2 + direction[1]**2
        angle = math.atan2(direction[1], direction[0])
        angle = angle * 180 / math.pi

        if (distance2 > THRESHRUN or run):
            # run
            self.controls.pressAngle(self.controlCenter, self.controlRadius[0],
                                     angle)
        else:
            # walk
            self.controls.pressAngle(self.controlCenter, self.controlRadius[1],
                                     angle)

    def goRoute(self):
        self.updateTarget()
        if self.routeIndex >= self.routeLen:
            self.controls.release()
            print("Arrived")
            return True
        direction = [
            self.route[self.routeIndex][0] - self.mapPos[0],
            self.route[self.routeIndex][1] - self.mapPos[1]
        ]
        if self.routeIndex == self.routeLen - 1:
            self.move(direction)
        else:
            nextDirection = self.route[self.routeIndex +
                                       1] - self.route[self.routeIndex]
            # normalize
            nextDirection = nextDirection / np.linalg.norm(nextDirection)
            direction = np.array(direction)
            direction = direction / np.linalg.norm(direction)
            dot = np.dot(direction, nextDirection)
            if dot > THRESHDIR:
                self.move(direction, True)
            else:
                self.move(direction)
        return False
