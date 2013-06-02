from pyirc.core.handlers.logs import LogHandler
import urllib, urllib2

class WebParser(object):
    def __init__(self, bot):
        self.bot = bot
        self.logger = LogHandler(__file__)
        self.logger.log("Class Initialized `WebParser`")
    def read(self, url):
        return urllib.urlopen(url).read()
    def garbage(self):
        pass