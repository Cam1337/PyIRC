import pyirc.core.objects.message as message
from pyirc.core.handlers.logs import LogHandler
import sys, traceback

class DataParser(object):
    def __init__(self, bot):
        self.logger = LogHandler(__file__)
        self.logger.log("Class Initialized `DataParser`")

        self.bot = bot
        self.message = message.Message(self.bot.nick)

    def privmsg(self, channel, data):
        self.logger.log("[PRIVMSG] Sending '{0}' to '{1}'".format(data, channel), lt=1)
        self.bot.send("PRIVMSG {0} :{1}".format(channel, data))

    def parse(self, msg):
        self.message.define(msg)
        nick_access = self.bot.accessHandler.get_access(self.message.unparsedNick)
        
        for module in self.bot.moduleHandler.modules:
            module = self.bot.moduleHandler.modules[module]
            for hook in module.hooks:
                kw, func, argc, access = hook
                if argc <= self.message.command_argc:
                    if  nick_access >= access:
                        if kw.compare(self.bot.command_char, self.message):
                            try:
                                func(self.message)
                            except Exception, e:
                                self.privmsg(self.message.location, "Exception {0} found.".format(str(e)))
                                for item in traceback.format_exc().split("\n"):
                                    if item.strip().startswith("File"):
                                        self.privmsg(self.message.location, self.bot.moduleHandler.error_clean(item))

    def garbage(self):
        pass