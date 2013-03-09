from pyirc.core.handlers.logs import LogHandler
from pyirc.modules._template.base import BaseModule, Keyword
from configuration import Configuration
from pyirc.core import utils
import random

class Card(object):
    def __init__(self,value,color):
        if not color:
            self.color = None
        else:
            self.color = color.lower()
        self.value = value.lower()
    def __repr__(self):
        return "[{0}:{1}]".format(self.color, self.value)
    def __str__(self):
        return "[{0}:{1}]".format(self.color, self.value)
    def compare(self, otherCard):
        return (otherCard.color == self.color) and (otherCard.value == self.value)

class Player(object):
    def __init__(self, nick):
        self.nick = nick
        self.cards = []
    def __str__(self):
        return self.nick

class Game(object):
    def __init__(self):
        self.is_running = False
        self.is_dealt = False

        self.players = []
        self.history = []

        self.current_player = None

        self.cards = self.assemble_deck()

    def random_card(self):
        return random.choice(self.cards)

    def dealall(self, count):
        for player in self.players:
            for cc in xrange(count):
                player.cards.append(self.random_card())

    def assemble_deck(self):
        colors, faces, specials, deck = ["r","b","g","y"], ["0","1","2","3","4","5","6","7","8","9","s","r","d2"], ["W","WD4"], []
        for color in colors:
            for face in faces:
                deck.append(Card(face,color))
        for face in specials:
            deck.append(Card(face, None))
        return deck

    def is_valid_card(self, card):
        for _c in self.cards:
            if card.compare(_c):
                return True

    def sanitize_play(self, param1, param2):
        if param1 in ["r","g","b","y"]:
            testCard = Card(param2, param1)
            if self.is_valid_card(testCard):
                return (True,testCard)
            else:
                return (False, "INVALID")
        if param1 in ["wd4","w"]:
            return Card(param1, None)


    def add_player(self, nick):
        player_exists = any([p.nick == nick for p in self.players])
        if not player_exists:
            self.players.append(Player(nick))
        return not player_exists

    def get_player(self, nick):
        for player in self.players:
            if player.nick == nick:
                return player


class Module(BaseModule): #UNO
    def __init__(self, bot):
        super(Module, self).__init__(bot, Configuration(self))

        # k, f, argc, axx
        self.hook(Keyword("uno",isCommand=True), self.hook_uno, 0, 0)
        self.hook(Keyword("join",isCommand=True), self.hook_join, 0, 0)
        self.hook(Keyword("deal",isCommand=True), self.hook_deal, 0, 0)
        self.hook(Keyword("stats",isCommand=True), self.hook_stats, 0, 0)
        self.hook(Keyword("cards",isCommand=True), self.hook_cards, 0, 0)
        self.hook(Keyword("play",isCommand=True), self.hook_play, 2, 0)

        self.game = Game()


    def privmsg_alert(self, message, gr=False, gd=False):
        if message.location == self.configuration.game_channel:
            if gr:
                if not self.game.is_running:
                    return self.privmsg(message.location, "{0}, no current game, type .uno to begin one!".format(message.nick))
            if gd:
                if not self.game.is_dealt:
                    return self.privmsg(message.location, "{0}, the cards have not been dealt, type .deal to deal the cards.".format(message.nick))
            return True
        self.notice(message.nick, "Please send all commands to me in the channel {0}".format(self.configuration.game_channel))

    def hook_uno(self, message):
        if self.privmsg_alert(message):
            if not self.game.is_running:
                self.game.is_running = True
                self.game.add_player(message.nick)
                self.privmsg(message.location,"Uno Game Started | Players in the game: {0}".format(utils.list_items(",", self.game.players)))
                self.privmsg(message.location,"To join the game type .join, to start type .deal")

    def hook_join(self, message):
        if self.privmsg_alert(message,True,False):
            added = self.game.add_player(message.nick)
            if added:
                self.privmsg(message.location,"{0} has joined the game!".format(message.nick))
            else:
                self.privmsg(message.location,"{0}, you are already playing.".format(message.nick))

    def hook_stats(self, message):
        if self.privmsg_alert(message,True,False):
            players = ["{0}[{1}]".format(p.nick, len(p.cards)) for p in self.game.players]
            self.privmsg(message.location, "Players: {0}".format(utils.list_items(",", players)))

    def send_cards(self, nick=False, player=False):
        if not player:
            player = self.game.get_player(nick)
        if player:
            self.notice(player.nick, ",".join(["[{0}:{1}]".format(c.color, c.value.upper()) for c in player.cards]))
        else:
            self.notice(player.nick, "Sorry, I don't think you have joined the game, type .join in {0} to join!".format(self.configuration.game_channel))

    def hook_deal(self, message):
        if self.privmsg_alert(message,True,False):
            self.game.is_dealt = True
            self.game.dealall(self.configuration.starting_cards)
            self.game.players[0].cards.extend([Card("5","r")])
            for player in self.game.players:
                self.game.current_player = self.game.players[0]
                self.send_cards(player=player)

    def hook_cards(self, message):
        if self.privmsg_alert(message, True, True):
            self.send_cards(message.nick)

    def hook_play(self, message):
        if self.privmsg_alert(message, True, True):
            is_valid, card = self.game.sanitize_play(message.commandArgs[0].lower(), message.commandArgs[1].lower())
            print type(card)