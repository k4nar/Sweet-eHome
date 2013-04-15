from mongokit import Connection
from logger import logger

try:
    connection = Connection('localhost', 27017)
    db = connection["sweet-ehome"]
except:
    logger.error("Can't connect to MongoDB at localhost:27017")
    exit(-1)
