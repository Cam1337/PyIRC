from pyirc.core.handlers.logs import LogHandler
import time

class Event(object):
    def __init__(self, trigger_time, function, args=None, callback=None, title=None):
        self.logger = LogHandler(__file__)
        self.trigger_time = trigger_time
        self.function = function
        self.args = args
        self.callback = callback
        self.title = title

        self.result = None
    def call(self):
        self.logger.log("Executing {0} from events".format(self.title or self.function), lt=3)
        if self.args:
            self.result = self.function(*args)
        else:
            self.result = self.function()
        if self.callback:
            self.callback(self.result)

class EventHandler(object):
    def __init__(self, bot):
        self.logger = LogHandler(__file__)
        self.logger.log("Class Initialized `EventHandler`")
        self.bot = bot
        self.events = []
    def schedule(self, in_seconds, function, args=None, callback=None, title=None):
        newEvent = Event(time.time() + in_seconds, function, args=args, callback=callback, title=title)
        self.events.append(newEvent)
    def check(self):
        for _event in self.events:
            if time.time() > _event.trigger_time:
                _event.call()