
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
    cooperation_payback = models.IntegerField()
    def group_formation(self):
        self.cooperation_payback = self.session.config['cooperation_payoff'] + self.session.config['victims_payoff']
        import random
        import numpy as np
        self.session.vars['nrounds'] = random.uniform (Constants.ll_rounds, Constants.ul_rounds)
        self.session.vars['mocks_done'] = False
        n = self.session.config['num_demo_participants']
        starting = np.random.normal(loc=self.session.config['initial_mean_energy_level'],scale=self.session.config['initial_std_energy_level'],size=n).round().astype('int').clip(100,200)
        for i in range(n):
            p = self.get_player_by_id(i+1)
            p.participant.payoff = int(starting[i])

class Player(BasePlayer):
    test1 = models.StringField(label='If you work alone, then by how much points can you expect your points level to gain that round?')
    def test1_choices(self):
        return [[f'{self.session.config["lone_payoff"]-10} points', f'{self.session.config["lone_payoff"]-10} points'], [f'{self.session.config["lone_payoff"]} points', f'{self.session.config["lone_payoff"]} points'], [f'{self.session.config["lone_payoff"]+10} points', f'{self.session.config["lone_payoff"]+10} points']]
    test2 = models.StringField(label='If you and one other person in the group decides to cooperate, and no-one decides to steal, on average, how much points can you expect to gain that round?')
    def test2_choices(self):
        return [[f'{self.session.config["cooperation_payoff"]-25} points', f'{self.session.config["cooperation_payoff"]-25} points'], [f'{self.session.config["cooperation_payoff"]} points', f'{self.session.config["cooperation_payoff"]} points'], [f'{self.session.config["cooperation_payoff"]+15} points', f'{self.session.config["cooperation_payoff"]+15} points']]
    test3 = models.StringField(label='Say your points level is 110, you decide to steal, everyone else in the group decides to cooperate, and you get away with it. What will your points level be, on average, after the round?')
    def test3_choices(self):
        return [[f'{110+self.session.config["steal_success_payoff"]-50} points', f'{110+self.session.config["steal_success_payoff"]-50} points'], [f'{110+self.session.config["steal_success_payoff"]-10} points', f'{110+self.session.config["steal_success_payoff"]-10} points'], [f'{110+self.session.config["steal_success_payoff"]} points', f'{110+self.session.config["steal_success_payoff"]} points']]
    consent = models.StringField(choices=[['Yes', 'Yes']], label='I consent to take part in this study. ', widget=widgets.RadioSelect)
    prolific_id = models.StringField(label='What is your Prolific ID?')
