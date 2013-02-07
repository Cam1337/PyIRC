from pyirc.modules._template.base import BaseModule
from pyirc.modules._template.base import Keyword
from configuration import Configuration

class Module(BaseModule):
    def __init__(self, bot):
        super(Module, self).__init__(bot, Configuration(self))

        self.hook(Keyword("test", isCommand=True), self.hook_test, 0, 0)

    def hook_test(self, message):
        self.privmsg(message.location,"test")
        self.action(message.location,"test")
        self.notice(message.location,"test")