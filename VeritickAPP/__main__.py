from vtKinterClass import vtKinterClass
import threading
import better_exceptions; better_exceptions.hook()
better_exceptions.MAX_LENGTH = None

myWindow = vtKinterClass()
threading.Thread(target=myWindow.start()).start()