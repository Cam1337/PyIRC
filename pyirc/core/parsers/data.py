import pyirc.core.objects.message as message
from pyirc.core.handlers.logs import LogHandler

class DataParser(object):
    def __init__(self, bot):
        self.logger = LogHandler(__file__)
        self.logger.log("Class Initialized `DataParser`")

        self.bot = bot
        self.message = message.Message(self.bot.nick)

    def parse(self, msg):
        self.message.define(msg)
        for module in self.bot.moduleHandler.modules:
            module = self.bot.moduleHandler.modules[module]
            for hook in module.hooks:
                kw, func, argc, access = hook
                if argc <= self.message.command_argc:
                    if self.bot.accessHandler.get_access(self.message.nick) >= access:
                        if kw.compare(self.bot.command_char, self.message):
                            try:
                                func(self.message)
                            except Exception, e:
                                print "\n\n", e, func, "\n\n"

    def garbage(self):
        pass