from pyirc.core.handlers.logs import LogHandler
from pyirc.core.data import database

class AccessHandler(object):
    def __init__(self, bot):
        self.bot = bot
        self.logger = LogHandler(__file__)
        self.logger.log("Class Initialized `AccessHandler`")
    def get_access(self, nick):
        return True
    def garbage(self):
        pass