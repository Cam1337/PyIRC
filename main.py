import pyirc.core.handlers.connection as connection
import pyirc.core.objects.bot as bot
import pyirc.core.objects.net as net

import pyirc.testing.moduleTester as moduleTester

class Main(object):
    def __init__(self):
        pass

    def test_uno(self):
        from pyirc.modules.uno import module as uno_module
        from pyirc.modules.uno import configuration as uno_config
        tester = moduleTester.TestHandler(uno_module, uno_config, com_char=".", bot_nick="TestBot", channel="##camcam")
        tester.send("cam",".uno")
        tester.send("josh",".join")
        tester.send("lee",".join")
        tester.send("cam",".stats")
        tester.send("cam",".deal")
        tester.send("cam",".draw")
        tester.send("cam",".draw")
        tester.send("cam",".draw")

    def run_bot(self):
        ircbot = bot.IRCBot("pircuno","pyirc","pyirc",None, ".")
        ircbot.set_network(net.Network("irc.codetalk.io",6667,["#lobby"],False))
        connectionManager = connection.ConnectionHandler()
        connectionManager.add(ircbot)
        connectionManager.mainloop()


if __name__ == "__main__":
    m = Main()
    # m.test_uno()
    m.run_bot()
