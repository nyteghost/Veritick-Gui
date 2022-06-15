import os
from mainWindow import vtKinterClass
import threading
import better_exceptions
import veriLog
from loguru import logger

import sys
better_exceptions.hook()
better_exceptions.MAX_LENGTH = None


path = "./logs"
isExist = os.path.exists(path)

if not isExist:
    os.makedirs(path)


logger.critical('__main__')


myWindow = vtKinterClass()
threading.Thread(target=myWindow.start()).start()
