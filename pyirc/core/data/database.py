from pyirc.core.handlers.logs import LogHandler
import MySQLdb

class Database(object):
    def __init__(self, path):
        self.dbpath = path
        self.logger = LogHandler(__file__)
        self.logger.log("HelperClass Initialized `Database`")