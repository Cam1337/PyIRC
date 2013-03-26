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
        self.is_wild = self.value == "wd4" or self.value == "w"
        self.offset = self.get_offset()
    def get_offset(self):
        if self.value in "0123456789w":
            return 1
        if self.value == "r":
            return -1
        if self.value in ["s","wd4","d2"]:
            return 2
    def __repr__(self):
        return "[{0}:{1}]".format(self.color, self.value)
    def __str__(self):
        return "[{0}:{1}]".format(self.color, self.value)
    def compare(self, otherCard):
        if otherCard.is_wild:
            return otherCard.value == self.value
        else:
            return (otherCard.color == self.color) and (otherCard.value == self.value)

class Player(object):
    def __init__(self, nick, all_cards):
        self.nick = nick
        self.cards = []
        self.all_cards = all_cards
    def __str__(self):
        return self.nick
    def has_card(self, other_card):
        for card in self.cards:
            if card.compare(other_card):
                return True
    def draw(self, number):
        newCards = []
        for i in xrange(number):
            choice = random.choice(self.all_cards)
            self.cards.append(choice)
            newCards.append(choice)
        return newCards
    def drop_card(self, card):
        removed = False
        for c in self.cards:
            if c.compare(card):
                if removed: return
                self.cards.remove(c)

    def get_cards(self,offset=0, c=None):
        if not c:
            c = self.cards
        return ",".join(["[{0}:{1}]".format(c.color or "*", c.value.upper()) for c in c[offset:]])


class Game(object):
    def __init__(self):
        self.is_running = False
        self.is_dealt = False

        self.players = []
        self.history = []

        self.current_player = None
        self.current_player_index = 0

        self.cards = self.assemble_deck()

    def reset(self):
        self.players = []
        self.history = []
        self.current_player_index = 0
        self.current_player = None
        self.is_running = False
        self.is_dealt = False

    @property
    def current_card(self):
        return self.history[-1]

    def random_card(self):
        return random.choice(self.cards)

    def dealall(self, count):
        for player in self.players:
            player.draw(count)
            player.cards.append(Card("8","r"))

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
            return (True, Card(param1, param2))
        return (None,None)


    def add_player(self, nick):
        player_exists = any([p.nick == nick for p in self.players])
        if not player_exists:
            self.players.append(Player(nick, self.cards))
        return not player_exists

    def get_player(self, nick):
        for player in self.players:
            if player.nick == nick:
                return player

    def next_player(self, offset):
        self.current_player_index =(self.current_player_index + offset) % len(self.players)
        self.current_player = self.players[self.current_player_index]
        if offset == 2:
            return self.players[self.current_player_index - 1]



class Module(BaseModule): #UNO
    def __init__(self, bot):
        super(Module, self).__init__(bot, Configuration(self))

        # k, f, argc, axx
        self.hook(Keyword("uno",isCommand=True), self.hook_uno, 0, 0)
        self.hook(Keyword("draw",isCommand=True), self.hook_draw, 0, 0)
        self.hook(Keyword("join",isCommand=True), self.hook_join, 0, 0)
        self.hook(Keyword("deal",isCommand=True), self.hook_deal, 0, 0)
        self.hook(Keyword("stats",isCommand=True), self.hook_stats, 0, 0)
        self.hook(Keyword("cards",isCommand=True), self.hook_cards, 0, 0)
        self.hook(Keyword("play",isCommand=True), self.hook_play, 2, 0)

        self.game = Game()


    def privmsg_alert(self, message, gr=False, gd=False):
        if message.location in self.configuration.game_channel:
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
            else:
                self.privmsg(message.location, )

    def hook_join(self, message):
        if self.privmsg_alert(message,True,False):
            if not self.game.is_dealt:
                added = self.game.add_player(message.nick)
                if added:
                    self.privmsg(message.location,"{0} has joined the game!".format(message.nick))
                else:
                    self.privmsg(message.location,"{0}, you are already playing.".format(message.nick))
            else:
                self.privmsg(message.location, "{0}, there is already a game running, please wait for the next one".format(message.nick))

    def hook_stats(self, message):
        if self.privmsg_alert(message,True,False):
            players = ["{0}[{1}]".format(p.nick, len(p.cards)) for p in self.game.players]
            self.privmsg(message.location, "Players: {0}".format(utils.list_items(",", players)))

    def send_cards(self, nick=False, player=False):
        if not player:
            player = self.game.get_player(nick)
        if player:
            self.notice(player.nick, "Cards: {0}".format(player.get_cards()))
        else:
            self.notice(player.nick, "Sorry, I don't think you have joined the game, type .join in {0} to join!".format(self.configuration.game_channel))

    def hook_deal(self, message):
        if self.privmsg_alert(message,True,False):
            if len(self.game.players) >= 2:
                self.game.is_dealt = True
                self.game.dealall(self.configuration.starting_cards)
                for player in self.game.players:
                    self.game.current_player = self.game.players[0]
                    self.send_cards(player=player)
                self.game.history.append(random.choice(self.game.cards))
                while self.game.history[-1].is_wild:
                    self.game.history[-1] = random.choice(self.game.cards)
                self.privmsg(message.location, "The top card is {0} and it is {1}'s turn!".format(self.game.history[-1], self.game.current_player))
            else:
                self.privmsg(message.location, "Not enough players! Two or more are needed.")

    def hook_cards(self, message):
        if self.privmsg_alert(message, True, True):
            self.send_cards(message.nick)

    def hook_draw(self, message):
        if self.privmsg_alert(message, True, True):
            card_player = self.game.get_player(message.nick)
            if self.game.current_player == card_player:
                drawn = card_player.draw(1)
                self.notice(card_player, "New cards: {0}".format(drawn))
            else:
                self.privmsg(message.location, "Sorry, it's not your turn")

    def hook_play(self, message):
        if self.privmsg_alert(message, True, True):
            card_player = self.game.get_player(message.nick)
            if self.game.current_player == card_player:
                is_valid, card = self.game.sanitize_play(message.commandArgs[0].lower(), message.commandArgs[1].lower())
                current_card = self.game.history[-1]
                if is_valid:
                    if self.game.current_player.has_card(card):
                        if card.is_wild:
                            self.play_logic(message, current_card, card, card_player)
                        else:
                            if current_card.value == card.value or current_card.color == card.color:
                                self.play_logic(message, current_card, card, card_player)
                            else:
                                self.privmsg(message.location, "That card does not play on {0}".format(current_card))
                    else:
                        self.privmsg(message.location, "{0}, you do not have that card".format(message.nick))
                else:
                    if card == "INVALID" or not card:
                        self.privmsg(message.location, "{0}, that is not a valid card to play.".format(message.nick))
            else:
                if card_player:
                    self.privmsg(message.location, "{0}, it is not your turn".format(message.nick))
                else:
                    self.privmsg(message.location, "{0}, you are not playing.".format(message.nick))

    def play_logic(self, message, current_card, card, card_player):
        self.game.history.append(card)
        if card.value == "s":
            skipped_player  = self.game.next_player(card.offset)
            self.privmsg(message.location, "{0} has been skipped.".format(skipped_player))
        if card.value == "d2":
            d2_player = self.game.next_player(card.offset)
            d2_player.draw(2)
            self.notice(d2_player, "Cards drawn: {0}".format(d2_player.get_cards(-2)))
            self.privmsg(message.location, "{0} draws two cards and is skipped.".format(d2_player))
        if card.value == "r":
            self.privmsg(message.location, "Play is reversed.")
            self.game.next_player(card.offset)
        if card.is_wild:
            if card.value == "wd4":
                d4_player = self.game.next_player(card.offset)
                d4_player.draw(4)
                self.notice(d4_player, "Cards drawn: {0}".format(d4_player.get_cards(-4)))
                self.privmsg(message.location, "{0} draws four cards and is skipped.".format(d4_player))
            if card.value == "w":
                self.game.next_player(card.offset)
        else:
            self.game.next_player(card.offset)
        self.privmsg(message.location, "Top card is now {0}, it is {1}'s turn".format(self.game.current_card, self.game.current_player))
        self.notice(self.game.current_player, "Cards: {0}".format(self.game.current_player.get_cards()))
        card_player.drop_card(card)
        if len(card_player.cards) == 0:
            self.privmsg(message.location, "Game over! {0} has won!!".format(card_player))
            self.game.reset()
        if len(card_player.cards == 1):
            self.privmsg(message.location, "{0} has 1 card left!!".format(card_player))