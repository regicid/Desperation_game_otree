
from otree.api import Currency as c, currency_range
from ._builtin import Page, WaitPage
from .models import Constants

class Debrief_page(Page):
    form_model = 'player'
    def vars_for_template(self):
        return dict(a = self.participant.payoff * 2 )
page_sequence = [Debrief_page]