log_show = [0,1,2,3,4]
# network configurations
host = "irc.freenode.net"
port = 6667
ssl = True
channels = ["##camcam"]

# bot configuration
nick = "pyIRC"
ident = "pyirc"
realname = "pyirc"
password = None

# access levels
accesss = [
                ("cam","*","unaffiliated/cam",10),
                ("adran","*","botters/staff/adran",3)
                ]

# plugins
dynamicPlugins = True
plugins = []