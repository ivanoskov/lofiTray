import subprocess
CREATE_NO_WINDOW = 0x08000000
subprocess.call("./LofiTray.exe", creationflags=CREATE_NO_WINDOW)