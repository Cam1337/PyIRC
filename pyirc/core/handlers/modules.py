from pyirc.core.handlers.logs import LogHandler
import os

f = "core"

class ModuleHandler(object):
    def __init__(self, bot, load_on_init=True):
        self.logger = LogHandler(__file__)
        self.logger.log("Class Initialized `ModuleHandler`")
        self.bot = bot
        self.modules = {}
        self.raw = {}

        self.to_load = []
        self.to_unload = []

        self.module_path = os.path.abspath(__file__.replace(os.path.split(__file__)[1],"../../modules"))

        if load_on_init:
            self.load_all_modules()

    def load_all_modules(self):
        ignore = ["__init__.py","__init__.pyc","_template"]
        modules = [f for f in os.listdir(self.module_path) if f not in ignore]
        for module in modules:
            self.load_module(module)

    def load_module(self, name):
        self.to_load.append(name)

    def load_module_actual(self, name):
        raw_import = __import__("pyirc.modules.{0}".format(name), fromlist=["module","configuration"], level=-1)
        module = raw_import.module.Module(self.bot, raw_import.configuration.Configuration)
        module.on_load()
        self.raw[name] = raw_import
        self.modules[name] = module

    def unload_module(self, name):
        self.to_unload.append(name)

    def unload_module_actual(self, name):
        if self.modules.get(name,None):
            self.modules[name].on_unload()
            del self.modules[name]
            del self.raw[name]

    def reload_module(self, name):
        reload(self.raw[name].module)
        reload(self.raw[name].configuration)
        self.modules[name] = self.raw[name].module.Module(self.bot, self.raw[name].configuration.Configuration)
        self.modules[name].on_load()

    def reload_all(self):
        for module in self.modules:
            self.reload_module(module)

    def garbage(self):
        for mod in self.to_unload:
            self.unload_module_actual(mod)
        for mod in self.to_load:
            self.load_module_actual(mod)
        self.to_unload, self.to_load = [], []
        for module in self.modules:
            self.modules[module].garbage()

    def error_clean(self, err):
        return err.split(os.path.split(os.path.split(self.module_path)[0])[0])[1][1:]