import cv2
import os
import numpy as np

src = "./MakeMap/output"
dst = "./MakeMap/final"

for filename in os.listdir(src):
    if not filename.endswith(".png"):
        continue

    print("src:", filename)
    image = cv2.imread(src + "/" + filename)

    # find the roi area that include the map
    map = np.where((image > [0, 0, 0]).all(axis=2))
    map = np.array(map)
    left = np.min(map[1])
    right = np.max(map[1])
    top = np.min(map[0])
    bottom = np.max(map[0])
    # flood fill the map area
    cv2.floodFill(image,
                  None, (0, 0), (200, 200, 200),
                  loDiff=(10, 10, 10),
                  upDiff=(50, 50, 50),
                  flags=4 | cv2.FLOODFILL_FIXED_RANGE)
    image = image[top:bottom, left:right]
    cv2.imwrite(dst + "/" + filename, image)
