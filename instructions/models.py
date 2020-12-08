
from otree.api import (
    models, widgets, BaseConstants, BaseSubsession, BaseGroup, BasePlayer,
    Currency as c, currency_range
)

doc = ''
class Constants(BaseConstants):
    name_in_url = 'instructions'
    players_per_group = None
    num_rounds = 1
    initial_mean_energy_level = c(105)
    ll_rounds = 8
    ul_rounds = 16
    ll_initial_energy_level = c(96)
    ul_initial_energy_level = c(120)
class Subsession(BaseSubsession):
    pass
class Group(BaseGroup):
    def group_formation(self):
        import random
        import numpy as np
        self.session.vars['nrounds'] = random.uniform (Constants.ll_rounds, Constants.ul_rounds)
        n = self.session.config['num_demo_participants']
        starting = np.random.normal(loc=self.session.config['initial_mean_energy_level'],scale=self.session.config['initial_std_energy_level'],size=n).round().astype('int')
        for i in range(n):
            p = self.get_player_by_id(i+1)
            p.participant.payoff = int(starting[i])

class Player(BasePlayer):
    test1 = models.StringField(choices=[['-10 points', '- 10 points'], ['0 points', '0 points'], ['+ 10 points', '+ 10 points']], label='If you work alone, then by how much can you expect your points level to change that round?')
    test2 = models.StringField(choices=[['- 30 points', '- 30 points'], ['+ 5 points', '+ 5 points'], ['+ 20 points', '+ 20 points']], label='If you and one other person in the group decides to cooperate, and no-one decides to steal, on average, by how much can you expect your points level to change that round?')
    test3 = models.StringField(choices=[['80 points', '80 points'], ['120 points', '120 points'], ['130 points', '130 points']], label='Say your points level is 110, you decide to steal, everyone else in the group decides to cooperate, and you get away with it. What will your points level be, on average, after the round?')
    consent = models.StringField(choices=[['Yes', 'Yes']], label='I consent to take part in this study. ', widget=widgets.RadioSelect)
    prolific_id = models.StringField(label='What is your Prolific ID?')
