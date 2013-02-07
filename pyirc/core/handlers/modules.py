from pyirc.core.handlers.logs import LogHandler
import os

class ModuleHandler(object):
    def __init__(self, bot, load_on_init=True):
        self.logger = LogHandler(__file__)
        self.logger.log("Class Initialized `ModuleHandler`")
        self.bot = bot
        self.modules = {}
        self.raw = {}
        self.module_path = os.path.abspath(__file__.replace(os.path.split(__file__)[1],"../../modules"))

        if load_on_init:
            self.load_modules()

    def load_modules(self):
        ignore = ["__init__.py","__init__.pyc","_template"]
        modules = [f for f in os.listdir(self.module_path) if f not in ignore]
        for module in modules:
            self.load_module(module)

    def load_module(self, name):
        raw_import = __import__("pyirc.modules.{0}".format(name), fromlist=["module"], level=-1)
        module = raw_import.module.Module(self.bot)
        module.on_load()
        self.raw[name] = raw_import
        self.modules[name] = module

    def unload_module(self, name):
        self.modules[name].on_unload()
        del self.modules[name]
        del self.raw[name]

    def reload_module(self, name):
        self.unload_module(name)
        self.load_module(name)