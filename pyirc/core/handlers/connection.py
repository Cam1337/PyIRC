from pyirc.core.handlers.logs import LogHandler
import socket
import select
import ssl

class ConnectionHandler(object):
    def __init__(self):
        self.logger = LogHandler(__file__)
        self.logger.log("Class Initialized `DataParser`")

        self.bots = []
        self.connections = []

    def add(self, bot):
        self.bots.append(bot)
    def remove(self, bot):
        self.bots.remove(bot)
    def connect(self, bot):
        self.logger.log("Connecting bot {0}".format(bot.nick), lt=1)
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
            bot.network.recvbuffer = ""
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
                if bot.network.is_connected:
                    self.logger.log("Connected bot {0}".format(bot.nick), lt=1)
                else:
                    self.logger.log("Failed to connect bot {0}".format(bot.nick), lt=4)

        self.bots = [bot for bot in self.bots if bot.network.is_connected]

        while len(self.bots) > 0:
            _send = [bot for bot in self.bots if bot.network.sendbuffer != []]

            _read, _write, _error = select.select(self.bots, _send, self.bots, 5)

            if _read:
                for bot in _read:
                    recv = self.recv(bot)
                    for data in recv:
                        self.logger.log("Received '{0}'".format(data.strip()), lt=3)
                        bot.dataParser.parse(data)

            if _write:
                for bot in _write:
                    for msg in bot.network.sendbuffer:
                        self.logger.log("Sending message '{0}'".format(msg.strip()), lt=3)
                        bot.network.socket.send(msg)
                        self.logger.log("Removing '{0}' from sendbuffer".format(msg.strip()), lt=5)
                    bot.network.sendbuffer = []

            if _error:
                for bot in _error:
                    self.disconnect(bot)
                    self.bots.remove(bot)


            for bot in self.bots:
                self.logger.log("Running garbage collection for {0}".format(bot), lt=1)
                bot.eventHandler.check()
                bot.dataParser.garbage()
                bot.webParser.garbage()
                bot.accessHandler.garbage()
                bot.moduleHandler.garbage()

        for bot in self.bots:
            self.disconnect(bot)

