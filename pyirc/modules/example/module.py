from pyirc.modules._template.base import BaseModule
from configuration import Configuration

class Module(BaseModule):
    def __init__(self):
        Super(Module, self).__init__(Configuration(self))