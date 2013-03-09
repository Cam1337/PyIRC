import pyirc.core.handlers.connection as connection
import pyirc.core.objects.bot as bot
import pyirc.core.objects.net as net

import pyirc.testing.moduleTester as moduleTester

import sys

if __name__ == "__main__":

    from pyirc.modules.uno import module as uno_module # module we will be testing

    tester = moduleTester.TestHandler(uno_module, com_char=".", bot_nick="TestBot", channel="#uno")
    tester.send("cam",".uno")
    tester.send("josh",".join")
    tester.send("lee",".join")
    tester.send("cam",".stats")
    tester.send("cam",".deal")
    tester.send("cam",".cards")
    tester.send("cam",".play r 5")




    sys.exit() # do not run bot, just do module test

    ircbot = bot.IRCBot("PyIRC","pyirc","pyirc",None, ".")

    ircbot.set_network(net.Network("irc.codetalk.io",6697,["#lobby"],True))

    connectionManager = connection.ConnectionHandler()

    connectionManager.add(ircbot)

    connectionManager.mainloop()