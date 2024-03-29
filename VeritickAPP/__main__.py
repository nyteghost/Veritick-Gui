import os
from _skeleton.mainWindow import vtKinterClass
import threading
import better_exceptions
from loguru import logger
from concurrent.futures import ThreadPoolExecutor

better_exceptions.hook()
better_exceptions.MAX_LENGTH = None

path = "./logs"
isExist = os.path.exists(path)

if not isExist:
    os.makedirs(path)

logger.critical('__main__')

myWindow = vtKinterClass()
# threading.Thread(target=myWindow.start()).start()

with ThreadPoolExecutor() as executor:
    executor.submit(myWindow.start())

