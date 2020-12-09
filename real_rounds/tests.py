from otree.api import Currency as c
from . import pages
from ._builtin import Bot
from .models import Constants

class PlayerBot(Bot):
    def play_round(self):
        yield pages.Decide, dict(decision="Work alone")
        yield pages.Outcome