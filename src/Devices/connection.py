from mongokit import Connection

try:
  from logger import logger
except:
  logger = None


HOST = 'localhost'
PORT = 27017

try:
    connection = Connection(host=HOST, port=PORT)
    db = connection["sweet-ehome"]
except:
    error = "Can't connect to MongoDB at {}:{}".format(HOST, PORT)

    if logger:
      logger.error(error)
    else:
      print error

    exit(-1)
