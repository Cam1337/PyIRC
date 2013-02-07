from pyirc.modules._template.base import BaseConfiguration

class Configuration(BaseConfiguration):
    def __init__(self, module):
        Super(Module, self).__init__(module)
        self.command_prefix = "example"