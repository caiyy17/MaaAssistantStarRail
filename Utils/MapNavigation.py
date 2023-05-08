import numpy as np
import cv2
from matplotlib import pyplot as plt

std_width: int = 1280
std_height: int = 720
search_width: int = 300
SMALL = 1.035
LARGE = 1.265


class MapNavigation:
    def __init__(self, controls, roi):
        self.roi = roi
        self.controls = controls
        self.screen = controls.screen
        self.controls.getScreen()
        # self.previous = self.getMap()
        # self.current = self.getMap()

    def setBigMap(self, bigMap):
        map = cv2.imread(bigMap)
        map = cv2.cvtColor(map, cv2.COLOR_BGR2GRAY)
        map = cv2.Canny(map, 300, 500)
        self.bigMap = cv2.Canny(map, 300, 500).astype(np.float64)
        cv2.imwrite("Screen/bigMap.png", self.bigMap)
        self.index = 0

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
        # print(screen_img.shape)
        return screen_img

    def getInitPos(self):
        self.current = self.getMap()
        img1 = self.current  # queryImage
        img1 = cv2.cvtColor(img1, cv2.COLOR_BGR2GRAY)
        edges1 = cv2.Canny(img1, 300, 500, 7).astype(np.float64)
        width = edges1.shape[0]
        scale = SMALL
        shift = (1 - scale) * width / 2
        test1 = cv2.warpAffine(
            edges1, np.float32([[scale, 0, shift], [0, scale, shift]]),
            (self.bigMap.shape[1], self.bigMap.shape[0]))
        offset, value = cv2.phaseCorrelate(test1, self.bigMap)
        currentOffset = [offset[0], offset[1]]
        if (offset[0] < 0):
            currentOffset[0] += self.bigMap.shape[1]
        if (offset[1] < 0):
            currentOffset[1] += self.bigMap.shape[0]
        res = cv2.warpAffine(
            test1,
            np.float32([[1, 0, currentOffset[0]], [0, 1, currentOffset[1]]]),
            (self.bigMap.shape[1], self.bigMap.shape[0]))
        cv2.imwrite(f"Screen/align0.jpg", self.bigMap - res + 128)
        self.offset = [
            currentOffset[0] - (search_width - width) / 2,
            currentOffset[1] - (search_width - width) / 2
        ]
        print(self.offset, value)

    def update(self):
        # self.previous = self.current
        self.current = self.getMap()
        self.index += 1
        # cv2.imwrite("Screen/previous.jpg", self.previous)
        # cv2.imwrite("Screen/current.jpg", self.current)
        # self.analyze()
        self.analyzeFull()

    def analyze(self):
        img1 = self.current  # queryImage
        # img2 = self.previous  # trainImage
        img1 = cv2.cvtColor(img1, cv2.COLOR_BGR2GRAY)
        # img2 = cv2.cvtColor(img2, cv2.COLOR_BGR2GRAY)
        edges1 = cv2.Canny(img1, 300, 500).astype(np.float64)
        # edges2 = cv2.Canny(img2, 300, 500).astype(np.float64)

        width = edges1.shape[0]
        gap = LARGE - SMALL
        steps = 20
        valueMax = 0
        currentScale = 0
        currentOffset = [0, 0]
        final1 = None
        for i in range(steps + 1):
            scale = SMALL + gap * i / steps
            shift = (search_width - scale * width) / 2
            test1 = cv2.warpAffine(
                edges1, np.float32([[scale, 0, shift], [0, scale, shift]]),
                (search_width, search_width))
            mapOffset = [-self.offset[0], -self.offset[1]]
            searchMap = cv2.warpAffine(
                self.bigMap,
                np.float32([[1, 0, mapOffset[0]], [0, 1, mapOffset[1]]]),
                (search_width, search_width))
            offset, value = cv2.phaseCorrelate(test1, searchMap)
            if value > valueMax:
                valueMax = value
                currentScale = scale
                currentOffset = [offset[0], offset[1]]
                final1 = test1
                # final2 = test2
        self.offset = [
            self.offset[0] + currentOffset[0],
            self.offset[1] + currentOffset[1]
        ]
        res = cv2.warpAffine(
            final1, np.float32([[1, 0, self.offset[0]], [0, 1,
                                                         self.offset[1]]]),
            (self.bigMap.shape[1], self.bigMap.shape[0]))
        cv2.imwrite(f"Screen/align{self.index}.jpg", self.bigMap - res + 128)
        print(valueMax, currentScale, currentOffset)

    def analyzeFull(self):
        img1 = self.current  # queryImage
        # img2 = self.previous  # trainImage
        img1 = cv2.cvtColor(img1, cv2.COLOR_BGR2GRAY)
        # img2 = cv2.cvtColor(img2, cv2.COLOR_BGR2GRAY)
        edges1 = cv2.Canny(img1, 300, 500).astype(np.float64)
        # edges2 = cv2.Canny(img2, 300, 500).astype(np.float64)

        width = edges1.shape[0]
        gap = LARGE - SMALL
        steps = 20
        valueMax = 0
        currentScale = 0
        currentOffset = [0, 0]
        final1 = None
        for i in range(steps + 1):
            scale = SMALL + gap * i / steps
            shift = (1 - scale) * width / 2
            test1 = cv2.warpAffine(
                edges1, np.float32([[scale, 0, shift], [0, scale, shift]]),
                (self.bigMap.shape[1], self.bigMap.shape[0]))
            offset, value = cv2.phaseCorrelate(test1, self.bigMap)
            if value > valueMax:
                valueMax = value
                currentScale = scale
                currentOffset = [offset[0], offset[1]]
                if (offset[0] < 0):
                    currentOffset[0] += self.bigMap.shape[1]
                if (offset[1] < 0):
                    currentOffset[1] += self.bigMap.shape[0]
                final1 = test1
                # final2 = test2
        res = cv2.warpAffine(
            final1,
            np.float32([[1, 0, currentOffset[0]], [0, 1, currentOffset[1]]]),
            (self.bigMap.shape[1], self.bigMap.shape[0]))
        cv2.imwrite(f"Screen/align{self.index}.jpg", self.bigMap - res + 128)
        print(valueMax, currentScale, currentOffset)