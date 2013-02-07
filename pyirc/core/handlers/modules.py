import os

class ModuleHandler(object):
    def __init__(self, bot, load_on_init=True):
        self.bot = bot
        self.modules = []
        self.module_path = os.path.abspath(__file__.replace(os.path.split(__file__)[1],"../../modules"))

        if load_on_init:
            self.load_modules()

    def load_modules(self):
        ignore = ["__init__.py","__init__.pyc","_template"]
        modules = [f for f in os.listdir(self.module_path) if f not in ignore]

    def load_module(self, module)