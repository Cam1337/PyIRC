from pyirc.core.handlers.logs import LogHandler

class AccessHandler(object):
    def __init__(self, bot):
        self.bot = bot
    def get_access(self, nick):
        return True