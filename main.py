import pyirc.core.handlers.connection as connection
import pyirc.core.objects.bot as bot
import pyirc.core.objects.net as net

import pyirc.testing.moduleTester as moduleTester

class Main(object):
    def __init__(self):
        pass

    def test_uno(self):
        from pyirc.modules.uno import module as uno_module
        tester = moduleTester.TestHandler(uno_module, com_char=".", bot_nick="TestBot", channel="#uno")
        tester.send("cam",".uno")
        tester.send("josh",".join")
        tester.send("lee",".join")
        tester.send("cam",".stats")
        tester.send("cam",".deal")
        tester.send("cam",".cards")
        tester.send("cam",".play r 8")
        tester.send("cam",".cards")

    def run_bot(self):
        ircbot = bot.IRCBot("PyIRCu","pyirc","pyirc",None, ".")
        ircbot.set_network(net.Network("irc.p2p-network.net",6667,["#scenetime"],False))
        connectionManager = connection.ConnectionHandler()
        connectionManager.add(ircbot)
        connectionManager.mainloop()


if __name__ == "__main__":
    m = Main()
    m.run_bot()
    # m.test_uno()
