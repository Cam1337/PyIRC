import inspect
import os
import config
import blessings

class LogHandler(object):
    def __init__(self, file):
        self.file = file.split("pyirc")[1]
        self.types = {0:"Log",1:"Info",2:"Error",3:"Debug",4:"Fatal Error"}


    def log(self, m=None, lt=0, ex=None):
        if lt not in config.log_show:
            return
        lt = self.types[lt]
        frame = inspect.getframeinfo(inspect.stack()[1][0])
        if m == None and ex == None:
            print "[{0}:{1}] Log Event".format(self.file, frame.lineno)
        else:
            print "[{0}:{1}] {2} :: {3}".format(self.file, frame.lineno, lt, m)