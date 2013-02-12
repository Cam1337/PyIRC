from pyirc.core.handlers.logs import LogHandler
from pyirc.modules._template.base import BaseModule
from pyirc.modules._template.base import Keyword
from configuration import Configuration

class Module(BaseModule):
    def __init__(self, bot):
        super(Module, self).__init__(bot, Configuration(self))

        self.hook(Keyword("test", isCommand=True), self.hook_test, 0, 0)
        self.hook(Keyword("PING", index=0, isArg=True), self.hook_ping, 0, 0)

    def hook_test(self, message):
        self.privmsg(message.location,"test")
        self.action(message.location,"test")
        self.notice(message.location,"test")

    def hook_ping(self, message):
        self.privmsg("##camcam", "Received ping: {0}".format(message.arg(1)))