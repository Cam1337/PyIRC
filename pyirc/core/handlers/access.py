from pyirc.core.handlers.logs import LogHandler
from pyirc.core.data import database

class AccessHandler(object):
    def __init__(self, bot):
        self.bot = bot
        self.logger = LogHandler(__file__)
        self.logger.log("Class Initialized `AccessHandler`")
    def get_access(self, nick, nm=True):
        if nm: nick = nick.lower()
        return self.get_real_access(nick)
    def get_real_access(self, nick):
        if nick in ["Nox","Cam", "Waflel"]:
            return True
        else:
            retrurn False
    def garbage(self):
        pass