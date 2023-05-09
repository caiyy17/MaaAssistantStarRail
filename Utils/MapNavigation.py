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


class MapNavigation:
    def __init__(self, controls, roi):
        self.roi = roi
        self.controls = controls
        self.screen = controls.screen
        self.controls.getScreen()

    def setBigMap(self, bigMap):
        map = cv2.imread(bigMap)
        self.bigMap = getEdge(map)
        cv2.imwrite("Screen/bigMap.png", self.bigMap)
        self.index = 0
        self.source = cv2.imread(bigMap)
        self.debug = self.source.copy()

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

    def update(self, debugMode=False):
        self.current = self.getMap()
        self.index += 1
        if not (self.analyze()):
            if debugMode:
                self.debug = self.source.copy()
            self.analyzeFull()
        if debugMode:
            cv2.circle(self.debug,
                       (int(self.offset[0] + self.current.shape[1] / 2),
                        int(self.offset[1] + self.current.shape[0] / 2)), 4,
                       (0, 0, 255), -1)
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