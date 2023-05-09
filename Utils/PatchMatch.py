import numpy as np
import cv2


def getEdge(img, low=300, high=500):
    img = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    edges = cv2.Canny(img, low, high).astype(np.float64)
    return edges


def patchMatch(target1, scale, target2):
    size = target1.shape
    shift = [(1 - scale) * size[1] / 2, (1 - scale) * size[0] / 2]
    shift = [(target2.shape[1] - scale * size[1]) / 2,
             (target2.shape[0] - scale * size[0]) / 2]
    target1 = cv2.warpAffine(
        target1, np.float32([[scale, 0, shift[0]], [0, scale, shift[1]]]),
        (target2.shape[1], target2.shape[0]))
    offset, value = cv2.phaseCorrelate(target1, target2)
    currentOffset = [
        offset[0] + (target2.shape[1] - size[1]) / 2,
        offset[1] + (target2.shape[0] - size[0]) / 2
    ]
    return currentOffset, value


def patchMatchScale(target1, small, large, steps, target2):
    size = target1.shape
    gap = large - small
    valueMax = -1
    for i in range(steps + 1):
        scale = small + gap * i / steps
        offset, value = patchMatch(target1, scale, target2)
        if value > valueMax:
            valueMax = value
            currentScale = scale
            currentOffset = [offset[0], offset[1]]
    return currentOffset, valueMax, currentScale