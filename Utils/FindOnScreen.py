import numpy as np
import cv2

std_width: int = 1280
std_height: int = 720


def findOnScreen(target, screen, threshold=0.8, roi=(-1, -1, -1, -1)):
    screen_img = cv2.imread(screen)
    target_img = cv2.imread(target)

    screen_img = cv2.resize(screen_img, (std_width, std_height),
                            interpolation=cv2.INTER_CUBIC)
    if roi == (-1, -1, -1, -1):
        roi = target.split("_")[-1].split(".")[0].split(",")
    # print(roi)
    left = int(roi[0])
    left = min(max(left, 0), std_width)
    top = int(roi[1])
    top = min(max(top, 0), std_height)
    right = left + int(roi[2])
    right = min(max(right, 0), std_width)
    bottom = top + int(roi[3])
    bottom = min(max(bottom, 0), std_height)
    # if not (0,0,0,0), crop roi
    if bottom != 0:
        screen_img = screen_img[top:bottom, left:right]

    ewsult = cv2.matchTemplate(screen_img, target_img, cv2.TM_CCOEFF_NORMED)
    min_val, max_val, min_loc, max_loc = cv2.minMaxLoc(ewsult)
    # print(max_loc)
    print(max_val)
    if max_val < threshold:
        return -1, -1
    x = int(left + max_loc[0] + target_img.shape[1] / 2)
    y = int(top + max_loc[1] + target_img.shape[0] / 2)
    return x, y