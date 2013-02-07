import socket
import select
import ssl

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
            bot.network.is_connected = True
            if bot.network.ssl:
                bot.network.socket = ssl.wrap_socket(bot.network.socket)
            bot.network.socket.connect((bot.network.host, bot.network.port))
            self.send(bot, "NICK {0}".format(bot.nick))
            self.send(bot, "USER {0} *** *** :{1}".format(bot.ident, bot.realname))
        except Exception, e:
            print e
            bot.network.is_connected = False
    def disconnect(self, bot):
        pass # to implement
    def send(self, bot, data):
        bot.send(data)
    def recv(self, bot):
        data = bot.network.socket.recv(1024)
        if bot.network.recvbuffer != "":
            data = bot.network.recvbuffer + data
        data = data.split("\r\n")
        if data[-1] != "":
            bot.network.recvbuffer = data[-1]
        else:
            data = data[:-1]
        return data
    def mainloop(self):
        for bot in self.bots:
            if not bot.network.is_connected:
                self.connect(bot)

        self.bots = [bot for bot in self.bots if bot.network.is_connected]

        while len(self.bots) > 0:
            _send = [bot for bot in self.bots if bot.network.sendbuffer != []]

            _read, _write, _error = select.select(self.bots, _send, self.bots, 5)

            if _read:
                for bot in _read:
                    recv = self.recv(bot)
                    for data in recv:
                        print "<-- {0}".format(data)
                        #bot.dataParser.parse(data)

            if _write:
                for bot in _write:
                    for msg in bot.network.sendbuffer:
                        print "--> {0}".format(msg.strip())
                        bot.network.socket.send(msg)
                        bot.network.sendbuffer.remove(msg)

            if _error:
                for bot in _error:
                    self.disconnect(bot)
                    self.bots.remove(bot)

        for bot in self.bots:
            self.disconnect(bot)

