import pyirc.core.handlers.connection as connection
import pyirc.core.objects.bot as bot
import pyirc.core.objects.net as net


if __name__ == "__main__":
    ircbot = bot.IRCBot("PyIRC","pyirc","pyirc",None, ".")

    ircbot.set_network(net.Network("irc.freenode.net",6667,["##camcam"],True))

    connectionManager = connection.ConnectionHandler()

    connectionManager.add(ircbot)

    connectionManager.mainloop()