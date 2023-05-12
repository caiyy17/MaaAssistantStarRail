import cv2
import os

# 初始化参考点列表和布尔值标志：是否正在执行裁剪
refPt = []
src = "./Screen/bigMap.png"
dst = "./Templates"


def getPoint(event, x, y, flags, param):
    # 声明全局变量
    global refPt
    if event == cv2.EVENT_LBUTTONDOWN:
        refPt.append((x, y))
        print(x, y)


cv2.namedWindow("image")
cv2.setMouseCallback("image", getPoint)

image = cv2.imread(src)
while True:
    cv2.imshow("image", image)
    key = cv2.waitKey(0) & 0xFF
    if key == ord("q"):
        break

# 关闭所有打开的窗口
cv2.destroyAllWindows()

print(refPt)
