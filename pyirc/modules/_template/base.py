class Keyword(object):
    def __init__(self, value, index=None, isArg=False, isCommand=False, caseSensitive=False):
        self.value  = value

        self.isArg = isArg
        self.index = index
        self.isCommand = isCommand
        self.caseSensitive = caseSensitive

    def compare(self, com_char, prefix, message):
        if self.isArg and self.index:
            val = message.arg(self.index)
        if self.isCommand:
            val = message.command
        if not self.caseSensitive:
            return val.lower() == com_char + ".".join([prefix, self.value]).lower()
        else:
            return val == com_char + ".".join([prefix, self.value])

class BaseModule(object):
    def __init__(self, bot, configuration):
        self.bot = bot
        self.configuration = configuration
        self.hooks = []
    def hook(self, keyword, function, argc, access):
        print "Adding hook: {0}".format(keyword.value)
        self.hooks.append((keyword, function, argc, access))
    def on_load(self):
        pass
    def on_unload(self):
        pass
    def privmsg(self, channel, data):
        self.bot.send("PRIVMSG {0} :{1}".format(channel, data))
    def action(self, channel, data):
        self.bot.send("PRIVMSG {0} :\x01ACTION {1}\x01".format(channel, data))
    def notice(self, channel, data):
        self.bot.send("NOTICE {0}: {1}".format(channel, data))

class BaseConfiguration(object):
    def __init__(self, module):
        self.command_prefix = None
        self.module = module

