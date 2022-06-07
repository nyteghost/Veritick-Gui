from vtKinterClass import *

myWindow = vtKinterClass()
# myWindow.start()

threading.Thread(target=myWindow.start()).start()