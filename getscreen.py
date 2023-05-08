from Utils.Controls import Controls

ADBADRESS = "127.0.0.1:5555"
ADB = "\"C:\Program Files\BlueStacks_nxt\.\HD-Adb.exe\""
SCREEN = "Screen/screen.png"

controls = Controls(ADB, ADBADRESS, SCREEN)
controls.connectADB()
controls.getScreen()