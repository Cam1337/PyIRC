from pyirc.modules._template import base

class Module(base.BaseModule):
    def __init__(self, config):
        Super(Module, self).__init__(config)