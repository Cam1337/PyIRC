from pyirc.core.handlers.logs import LogHandler

class Keyword(object):
    def __init__(self, value, index=None, prefix=None, isArg=False, isCommand=False, caseSensitive=False):
        self.value  = value
        self.prefix = prefix
        self.isArg = isArg
        self.index = index
        self.isCommand = isCommand
        self.caseSensitive = caseSensitive

    def compare(self, com_char, message):
        if self.isArg and self.index != None:
            val = message.arg(self.index)
            sv = self.value
        if self.isCommand:
            val = message.command
            if self.prefix:
                sv = com_char + ".".join([self.prefix, self.value]).lower()
            else:
                sv = com_char + self.value.lower()
        if not self.caseSensitive and sv and val:
            return val.lower() == sv.lower()
        return val == sv

    def __repr__(self):
        if self.isArg and self.index != None:
            return self.value
        if self.isCommand:
            if self.prefix:
                return ".".join([self.prefix, self.value]).lower()
            else:
                return self.value.lower()
        return "Unknown"

class BaseModule(object):
    def __init__(self, bot, configuration):
        self.logger = LogHandler(__file__)
        self.bot = bot
        self.configuration = configuration
        self.hooks = []
    def hook(self, keyword, function, argc, access):
        keyword.prefix = self.configuration.command_prefix
        self.logger.log("Added hook '{0}'".format(keyword), lt=3)
        self.hooks.append((keyword, function, argc, access))
    def on_load(self):
        self.logger.log("on_load() for '{0}'".format(self.configuration.command_prefix), lt=3)
    def on_unload(self):
        self.logger.log("on_unload() for '{0}'".format(self.configuration.command_prefix), lt=3)
    def send(self, data):
        self.bot.send(data)
    def privmsg(self, channel, data):
        self.logger.log("[PRIVMSG] Sending '{0}' to '{1}'".format(data, channel), lt=1)
        self.bot.send("PRIVMSG {0} :{1}".format(channel, data))
    def action(self, channel, data):
        self.logger.log("[ACTION] Sending '{0}' to '{1}'".format(data, channel), lt=1)
        self.bot.send("PRIVMSG {0} :\x01ACTION {1}\x01".format(channel, data))
    def notice(self, channel, data):
        self.logger.log("[NOTICE] Sending '{0}' to '{1}'".format(data, channel), lt=1)
        self.bot.send("NOTICE {0} :{1}".format(channel, data))

class BaseConfiguration(object):
    def __init__(self, module):
        self.command_prefix = None
        self.module = module

