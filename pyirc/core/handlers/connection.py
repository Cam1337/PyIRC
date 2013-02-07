import socket
import select

class ConnectionHandler(object):
    def __init__(self):
        self.bots = []
        self.connections = []

    def add(self, bot):
        self.bots.append(bot)
    def remove(self, bot):
        self.bots.remove(bot)
    def connect(self, bot):
        try:
            bot.network.socket.connect((bot.network.host, bot.network.port))
            self.send(bot, "NICK {0}".format(bot.nick))
            self.send(bot, "USER {0} *** *** :{1}".format(bot.ident, bot.realname))
            bot.network.is_connected = True
        except Exception, e:
            bot.network.is_connected = False
    def disconnect(self, bot):
        pass # to implement
    def send(self, bot, data):
        if bot.network.is_connected:
            bot.senduffer.append("{0}\r\n".format(data))
    def recv(self, bot):
        data = bot.network.socket.recv(1024)
        if self.bot.network.
    def mainloop(self):
        for bot in self.bots:
            if not bot.network.is_connected:
                self.connect(bot)
        print [bot.network.is_connected for bot in self.bots]
        self.bots = [bot for bot in self.bots if bot.network.is_connected]
        while len(self.bots) > 0:
            _send = [bot.network for bot in self.bots if bot.network.sendbuffer != []]
            _nets  = [bot.network for bot in self.bots]

            _read, _write, _error = select.select(_nets, _send, _nets, 5)

            if _read:
                for bot in _read:
                    recv = self.recv(bot)
                    for data in recv:
                        bot.dataParser.parse(data)

            if _write:
                for bot in _write:
                    for msg in bot.network.sendbuffer:
                        bot.network.socket.send(msg)

            if _error:
                for bot in _error:
                    self.disconnect(bot)
                    self.bots.remove(bot)

        for bot in self.bots:
            self.disconnect(bot)

