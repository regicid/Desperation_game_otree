
from otree.api import Currency as c, currency_range
from ._builtin import Page, WaitPage
from .models import Constants

class Decide(Page):
    form_model = 'player'
    form_fields = ['decision']
    timeout_seconds = 60
    timeout_submission = {'decision': 'Work alone'}
class Wait_for_decision(WaitPage):
    after_all_players_arrive = 'reckoning'
    body_text = 'Waiting for other group members....'
class Outcome(Page):
    form_model = 'player'
    def app_after_this_page(self, upcoming_apps):
        
        target_rounds = self.session.config['number_mock_rounds'] 
        if self.round_number + 1 > target_rounds:
            return upcoming_apps[0]

        
page_sequence = [Decide, Wait_for_decision, Outcome]
