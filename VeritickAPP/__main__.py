from vtKinterClass import *
import better_exceptions; better_exceptions.hook()
better_exceptions.MAX_LENGTH = None



myWindow = vtKinterClass()
# myWindow.start()

threading.Thread(target=myWindow.start()).start()