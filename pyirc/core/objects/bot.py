import pyirc.core.handlers.access as access
import pyirc.core.handlers.event as event
import pyirc.core.handlers.modules as modules
import pyirc.core.parsers.data as data


class IRCBot(object):
    def __init__(self, nick, ident, realname, password, comchar):
        self.nick = nick
        self.ident = ident
        self.realname = realname
        self.password = password
        self.auth = (self.password != None)
        self.network = None
        self.sendbuffer = []

        self.moduleHandler = modules.ModuleHandler(self)
        self.accessHandler = access.AccessHandler(self)
        self.eventHandler = event.EventHandler(self)
        self.dataParser = data.DataParser(self)

        self.command_char = comchar

    def set_network(self, network):
        self.network = network
        self.network.socket.settimeout(network.timeout)

    def fileno(self):
        return self.socket.fileno()