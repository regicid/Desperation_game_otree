
from otree.api import (
    models, widgets, BaseConstants, BaseSubsession, BaseGroup, BasePlayer,
    Currency as c, currency_range
)

doc = ''
class Constants(BaseConstants):
    name_in_url = 'debrief'
    players_per_group = None
    num_rounds = 1
class Subsession(BaseSubsession):
    pass
class Group(BaseGroup):
    def reckoning(self):
    	players = self.get_players()
    	for player in players:
    		player.cash_bonus = np.array(self.session.config['real_world_currency_per_point']*int(player.participant.payoff) - 
                self.session.config["penalty"]*player.participant.vars['rounds_below_threshold']).clip(0)
            


class Player(BasePlayer):
    pass