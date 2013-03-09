from pyirc.modules._template.base import BaseConfiguration

class Configuration(BaseConfiguration):
    def __init__(self, module):
        super(Configuration, self).__init__(module)
        self.command_prefix = None
        self.game_channel = "#uno"
        self.starting_cards = 7