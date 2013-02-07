from pyirc.core.handlers.logs import LogHandler

class Message(object):
    def __init__(self, nick):
        self.logger = LogHandler(__file__)
        self.logger.log("Class Initialized `message`")

        self.bot_nick = nick

        self.args         = []
        self.argc        = len(self.args)
        self.line         = ""
        self.unparsedNick = ""
        self.nick         = ""
        self.location     = ""
        self.destination  = ""
        self.command      = ""
        self.commandArgs  = ""
        self.hostName     = ""

    def arg(self, argNum):
        try:
            return self.args[argNum]
        except Exception, e:
            return None

    def define(self, data):
        self.args = data.split()
        self.argc = len(self.args)
        self.line = " ".join(self.args)

        try:
            self.unparsedNick = (self.args[0].split("!")[0]).lstrip(":")
        except IndexError:
            self.unparsedNick = ""

        self.nick = self.unparsedNick.lower()

        try:
            if self.args[2].lower() == self.bot_nick.lower():
                self.location = self.nick
            else:
                self.location = self.args[2].strip(":").lower()
        except IndexError:
            self.location = ""

        self.destination = self.location

        try:
            self.command = (self.args[3])[1:]
        except IndexError, e:
            self.command = ""

        try:
            self.commandArgs = self.args[4:]
        except IndexError:
            self.commandArgs = ""

        try:
            self.hostName = self.args[0].split("@")[1]
        except IndexError:
            self.hostName = ""
