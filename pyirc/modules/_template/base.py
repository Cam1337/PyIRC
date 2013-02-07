class BaseModule(object):
    def __init__(self, configuration):
        self.configuration = configuration
    def on_load(self):
        pass
    def on_unload(self):
        pass

class BaseConfiguration(object):
    def __init__(self, module):
        self.command_prefix = None
        self.module = module

