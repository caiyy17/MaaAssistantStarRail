import numpy as np
import cv2
from matplotlib import pyplot as plt
import os

src = "./MakeMap/input"
dst = "./MakeMap/output"
mapName = "111"

mapRes = 2000
mapSize = (mapRes, mapRes)
mapOffset = (100, 100)
roi = (140, 150, 600, 400)


def makeMap():
    fileList = os.listdir(src)
    base = cv2.imread(src + "/" + fileList[0])
    # base = base[roi[1]:roi[1] + roi[3], roi[0]:roi[0] + roi[2]]
    baseEdge = cv2.Canny(base, 100, 200)
    base = cv2.warpAffine(
        base, np.float32([[1, 0, mapOffset[0]], [0, 1, mapOffset[1]]]),
        mapSize, cv2.INTER_CUBIC)
    baseEdge = cv2.warpAffine(
        baseEdge, np.float32([[1, 0, mapOffset[0]], [0, 1, mapOffset[1]]]),
        mapSize, cv2.INTER_CUBIC).astype(np.float64)
    # cv2.imwrite(dst + "/base.png", base)
    # cv2.imwrite(dst + "/edge.png", baseEdge)
    for filename in fileList[1:]:
        if not filename.endswith(".png"):
            continue
        print("src:", filename)
        image = cv2.imread(src + "/" + filename)
        # image = image[roi[1]:roi[1] + roi[3], roi[0]:roi[0] + roi[2]]
        imageEdge = cv2.Canny(image, 100, 200)
        image = cv2.warpAffine(image, np.float32([[1, 0, 0], [0, 1, 0]]),
                               mapSize)
        imageEdge = cv2.warpAffine(imageEdge, np.float32([[1, 0, 0], [0, 1,
                                                                      0]]),
                                   mapSize).astype(np.float64)
        # cv2.imwrite(dst + "/image.png", image)
        # cv2.imwrite(dst + "/imageEdge.png", imageEdge)
        offset = np.array(cv2.phaseCorrelate(imageEdge, baseEdge)[0])
        if (offset[0] < -mapRes / 2):
            offset[0] += mapRes
        if (offset[1] < -mapRes / 2):
            offset[1] += mapRes
        image = cv2.warpAffine(
            image, np.float32([[1, 0, offset[0]], [0, 1, offset[1]]]), mapSize)
        imageEdge = cv2.warpAffine(
            imageEdge, np.float32([[1, 0, offset[0]], [0, 1, offset[1]]]),
            mapSize).astype(np.float64)
        base = cv2.max(base, image)
        baseEdge = cv2.max(baseEdge, imageEdge)
        # cv2.imwrite(dst + "/map.png", base)
    # make black (0,0,0) pixels white
    # base[np.where((base < [30, 30, 30]).all(axis=2))] = [210, 210, 210]
    cv2.imwrite(dst + f"/BigMap{mapName}.png", base)


makeMap()
