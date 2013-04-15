import logging
from logging.handlers import RotatingFileHandler

logger = logging.getLogger()
logger.setLevel(logging.WARNING)

formatter = logging.Formatter('%(asctime)s :: %(levelname)s :: %(message)s')
file_handler = RotatingFileHandler('logs/activity.log', 'a', 1000000, 1)
file_handler.setLevel(logging.WARNING)
file_handler.setFormatter(formatter)
logger.addHandler(file_handler)

steam_handler = logging.StreamHandler()
steam_handler.setLevel(logging.WARNING)
logger.addHandler(steam_handler)
