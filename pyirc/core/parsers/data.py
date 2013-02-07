import pyirc.core.objects.message as message

class DataParser(object):
    def __init__(self, bot):
        self.bot = bot
        self.message = message.Message(self.bot.nick)
    def parse(self, msg):
        self.message.define(msg)
        if self.message.arg(1) == "001":
            self.bot.send("JOIN ##camcam")
        for module in self.bot.moduleHandler.modules:
            module = self.bot.moduleHandler.modules[module]
            for hook in module.hooks:
                kw, func, argc, access = hook
                if argc <= self.message.argc:
                    if self.bot.accessHandler.get_access(self.message.nick) >= access:
                        if kw.compare(self.bot.command_char, module.configuration.command_prefix, self.message):
                            func(self.message)