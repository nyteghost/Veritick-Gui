import os
from vtKinterClass import vtKinterClass
import threading
import better_exceptions
from loguru import logger

better_exceptions.hook()
better_exceptions.MAX_LENGTH = None


path = "./logs"
isExist = os.path.exists(path)

if not isExist:
    os.makedirs(path)

logger.add("./logs/__main__.log", backtrace=True, diagnose=True, rotation="12:00")


myWindow = vtKinterClass()
threading.Thread(target=myWindow.start()).start()
