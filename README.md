# MaaAssistantStarRail

This is a small toy python repo inspired by the idea of MaaAssistantArknights. But the code is completely irrelevant to the original Maa project.

Examples can be found in the main.py. Please set your own ADB address. Note that I use sendevent for continous character control, while different ADB and devices can have different ADB sendevent behaviour. Your should change the sendevent config in the Utils/params.py file if your ADB is different.

# Auto tasks

use GameTasks.doTask(f"taskSub{tabIndex}", f"taskSub{taskIndex}", num) to automatically do tasks.
Currently taskTab2-6 is supported.

# Map location finding

Use MapNavigation.update() to get the real-time location of the tiny map. In debugMode, the location will be illustrated in the Screen/debug.jpg. Using sendevent enable me to do continous character control while still receiving the screencap from the simulator. Basically the time gap between 2 screencap is about 1 second.
