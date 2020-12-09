
from otree.api import Currency as c, currency_range
from ._builtin import Page, WaitPage
from .models import Constants

class Consent(Page):
    form_model = 'player'
    form_fields = ['prolific_id', 'consent']
class Form_groups(WaitPage):
    after_all_players_arrive = 'group_formation'
class Instructions(Page):
    form_model = 'player'
    form_fields = ['test1', 'test2', 'test3']
page_sequence = [Consent, Form_groups,Instructions]
