from otree.api import Currency as c
from . import pages
from ._builtin import Bot
from .models import Constants

class PlayerBot(Bot):
    def play_round(self):
        yield pages.Consent, dict(prolific_id="xyz", consent="Yes")
        yield pages.Instructions, dict(
            test1="-10 points",
            test2="- 30 points",
            test3="75 points",
        )