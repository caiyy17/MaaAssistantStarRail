import cv2
import os

# 初始化参考点列表和布尔值标志：是否正在执行裁剪
refPt = []
cropping = False

src = "./Screen"
dst = "./Templates"


# 点击并裁剪ROI区域
# -events 鼠标事件（如按下鼠标左键，释放鼠标左键，鼠标移动等）
# -x x坐标
# -y y坐标
# -flages params 其他参数
def click_and_crop(event, x, y, flags, param):
    if event == cv2.EVENT_LBUTTONDOWN:
        print(x, y)


print(
    "Usage:\n"
    "Put the 16:9 images under ./src, and run this script, it will be auto converted to 720p.\n"
    "Drag mouse to select ROI, press 'S' to save, press 'Q' to quit.\n"
    "The cropped images will be saved in ./dst\n")

std_width: int = 1280
std_height: int = 720
std_ratio = std_width / std_height

cv2.namedWindow("image")
cv2.setMouseCallback("image", click_and_crop)

for filename in os.listdir(src):
    if not filename.endswith(".png"):
        continue

    print("src:", filename)
    image = cv2.imread(src + "/" + filename)
    image = cv2.resize(image, (std_width, std_height),
                       interpolation=cv2.INTER_CUBIC)

    while True:
        cv2.imshow("image", image)
        key = cv2.waitKey(0) & 0xFF
        if key == ord("s"):
            break
        elif key == ord("q"):
            exit()

# 关闭所有打开的窗口
cv2.destroyAllWindows()
