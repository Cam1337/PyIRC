#logger(ltype.ERR, __file__, line, tback, e)

import inspect, os

class ltype(object):
    ERR = "Error"
    LOG = "Log"
    FER = "Fatal Error"
    INF = "Info"
    DBG = "Debug"


class LogHandler(object):
    def __init__(self, file):
        self.file = file.split("pyirc")[1]


    def log(self, m=None, ex=None, lt=ltype.LOG):
        frame = inspect.getframeinfo(inspect.stack()[1][0])
        if m == None and ex == None:
            print "[{0}:{1}] Log Event".format(self.file, frame.lineno)
        else:
            print "[{0}:{1}] {2} :: {3}".format(self.file, frame.lineno, lt, m)