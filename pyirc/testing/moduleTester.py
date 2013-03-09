from pyirc.core.objects import message as message
import blessings, inspect

class PseudoBot(object):
    def __init__(self, nick, location, terminal):
        self.terminal = terminal
        self.location = location
        self.nick = nick
        self.buff = []
    def send(self, data):
        self.buff.append((self.nick, data))
    def sendall(self):
        for _ in range(len(self.buff)):
            nick, data = self.buff.pop(0)
            data = "{0}!{0}@tester.localhost ".format(self.nick) + data
            self._print(nick,data, data.split()[2])
    def _print(self, nick, message, location):
        print self.terminal.underline_yellow("[{0}]:{1}".format(location, message.split()[1])), self.terminal.cyan("<{0}>".format(nick)), self.terminal.bright_red(":".join(message.split(":")[1:]))


class TestHandler(object):
    def __init__(self, module, com_char, bot_nick, channel, access_func=lambda a: 1):
        self.terminal = blessings.Terminal()

        self.pseudo_bot = PseudoBot(bot_nick, channel, self.terminal)
        self.message = message.Message("TestBot")

        self.channel = channel

        self.com_char = com_char
        self.access_func = access_func

        self.initialize(module)


    def initialize(self, module):
        self.module = module.Module(self.pseudo_bot)

    def match(self, func, retval, access, argc, kw):
        margc, argc = argc
        maccess, access = access
        print "\t Match found : {0}{1}".format(self.terminal.green(func.__name__), self.terminal.green("()"))
        print "\t `-- File    : {0}".format(self.terminal.green("/".join(inspect.getfile(func).split("/")[-3:-1])))
        print "\t `-- Return  : {0}".format(self.terminal.green(str(retval)))
        print "\t `-- Access  : {0}".format(self.terminal.green("{0} for level {1} required".format(maccess, access)))
        print "\t `-- Args    : {0}".format(self.terminal.green("{0} of {1} required".format(margc, argc)))
        print "\t `-- Command : {0}".format(self.terminal.green(str(kw.isCommand)))

    def send(self, sender, message):
        data_str = "{0}!{0}@tester.localhost PRIVMSG {1} :{2}".format(sender, self.channel, message)
        self.message.define(data_str)

        self.pseudo_bot._print(self.message.nick, self.message.line, self.channel)

        for hook in self.module.hooks:
            kw, func, argc, access = hook
            if argc <= self.message.argc:
                if self.access_func(self.message.nick) >= access:
                    if kw.compare(self.com_char, self.message):
                        retval = func(self.message)
                        self.match(func, retval, (self.access_func(self.message.nick), access), (len(self.message.commandArgs), argc), kw)
                        self.pseudo_bot.sendall()


