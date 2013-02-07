import socket

class Network(object):
    def __init__(self, host, port, channels, ssl=False, timeout=5):
        self.host = host
        self.port = port
        self.channels = channels
        self.ssl = ssl
        self.timeout = timeout

        self._host = ""
        self._version = ""
        self.specifics = {}

        self.socket = socket.socket()

        self.sendbuffer = []
        self.recvbuffer = ""

        self.is_connected = False

    def fileno(self):
        return self.socket.fileno()

    def parse_protocol_string(self, protocol_string):
        pass

        """:sendak.freenode.net 002 Cam_ :Your host is sendak.freenode.net[193.219.128.49/6667], running version ircd-seven-1.1.3
:sendak.freenode.net 003 Cam_ :This server was created Mon Dec 31 2012 at 23:37:24 EET
:sendak.freenode.net 004 Cam_ sendak.freenode.net ircd-seven-1.1.3 DOQRSZaghilopswz CFILMPQbcefgijklmnopqrstvz bkloveqjfI
:sendak.freenode.net 005 Cam_ CHANTYPES=# EXCEPTS INVEX CHANMODES=eIbq,k,flj,CFLMPQcgimnprstz CHANLIMIT=#:120 PREFIX=(ov)@+ MAXLIST=bqeI:100 MODES=4 NETWORK=freenode KNOCK STATUSMSG=@+ CALLERID=g :are supported by this server
:sendak.freenode.net 005 Cam_ CASEMAPPING=rfc1459 CHARSET=ascii NICKLEN=16 CHANNELLEN=50 TOPICLEN=390 ETRACE CPRIVMSG CNOTICE DEAF=D MONITOR=100 FNC TARGMAX=NAMES:1,LIST:1,KICK:1,WHOIS:1,PRIVMSG:4,NOTICE:4,ACCEPT:,MONITOR: :are supported by this server
:sendak.freenode.net 005 Cam_ EXTBAN=$,arx WHOX CLIENTVER=3.0 SAFELIST ELIST=CTU :are supported by this server"""