from pyirc.core.handlers.logs import LogHandler
from pyirc.modules._template.base import BaseModule
from pyirc.modules._template.base import Keyword


from pyirc.core import utils

class Module(BaseModule): #CORE
    def __init__(self, bot, configuration):
        super(Module, self).__init__(bot, configuration(self))

        self.hook(Keyword("test", isCommand=True), self.hook_test, 0, 0)
        self.hook(Keyword("ping", index=0, isArg=True), self.hook_ping, 0, 0)
        self.hook(Keyword("ping",isCommand=True), self.hook_user_ping, 0, 0)
        self.hook(Keyword("reload",isCommand=True), self.hook_reload, 0, 0)
        self.hook(Keyword("001", index=1, isArg=True), self.hook_001, 1, 0)

    def hook_001(self, message):
        for channel in self.bot.network.channels:
            self.send("JOIN {0}".format(channel))

    def hook_user_ping(self, message):
        self.privmsg(message.location,"pong")

    def hook_test(self, message):
        self.privmsg(message.location,"test")
        self.action(message.location,"test")
        self.notice(message.location,"test")

    def hook_ping(self, message):
        self.send("pong {0}".format(message.arg(1)))

    def hook_reload(self, message):
        self.bot.moduleHandler.reload_all()