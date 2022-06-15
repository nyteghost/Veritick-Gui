from loguru import logger

logger.add("./logs/__veriLog__.log", backtrace=True,
           diagnose=True,
           format="{time}-{message}", rotation="1 week", enqueue=True)
