
from otree.api import (
    models, widgets, BaseConstants, BaseSubsession, BaseGroup, BasePlayer,
    Currency as c, currency_range
)

doc = ''
class Constants(BaseConstants):
    name_in_url = 'mock_rounds'
    players_per_group = 2
    num_rounds = 20
    steal_success_prob = 0.333
    cooperation_payoff = c(5)
    energy_cost = c(0)
    energy_stochasticity = 3
    victims_payoff = c(0)
    steal_success_payoff = c(20)
    steal_failure_payoff = c(-40)
    lone_payoff = c(0)
    threshold = c(100)
    penalty = c(10)
class Subsession(BaseSubsession):
    def creating_session(self):
        self.group_randomly() 
class Group(BaseGroup):
    num_stealers = models.IntegerField()
    num_cooperators = models.IntegerField()
    coin_toss = models.FloatField()
    nrounds = models.FloatField()
    def reckoning(self):
        import random
        import numpy as np
        self.coin_toss = random.uniform(0, 1)
                
        players = self.get_players()
                
        stealers = []
        for player in players:
            if player.decision == 'Steal':
                stealers.append(player)
        self.num_stealers = len(stealers)
                
        cooperators = []
        for player in players:
            if player.decision == 'Cooperate':
                cooperators.append(player)
        self.num_cooperators = len(cooperators)
                
        for player in players:
            random_energy_cost = int(np.clip(np.random.normal(loc=Constants.energy_cost,scale=Constants.energy_stochasticity),-20,0).round())
            if player.decision == 'Work alone':
                player.delta_energy_level = random_energy_cost + Constants.lone_payoff
                player.outcome = 'You worked alone.'
            elif player.decision == 'Cooperate' and self.num_cooperators < 2 and self.num_stealers == 0:
                player.delta_energy_level = random_energy_cost + Constants.lone_payoff
                player.outcome = 'No-one else wanted to cooperate. You had to work alone'
            elif player.decision == 'Cooperate' and self.num_cooperators > 1 and self.num_stealers == 0:
                player.delta_energy_level = random_energy_cost + Constants.cooperation_payoff
                player.outcome = 'You cooperated successfully.'
            elif player.decision == 'Cooperate' and self.num_stealers > 0:
                if self.coin_toss < Constants.steal_success_prob:
                    player.delta_energy_level = random_energy_cost + Constants.victims_payoff
                    player.outcome = 'You were stolen from.'
                else: 
                    player.delta_energy_level = random_energy_cost + Constants.cooperation_payoff
                    player.outcome = 'Someone tried to steal but you caught them.'
            elif player.decision == 'Steal' and self.num_cooperators > 0:
                if self.coin_toss < Constants.steal_success_prob:
                    player.delta_energy_level = random_energy_cost + Constants.steal_success_payoff
                    player.outcome = 'You stole successfully.'
                else: 
                    player.delta_energy_level = random_energy_cost + Constants.steal_failure_payoff
                    player.outcome = 'You tried to steal but got caught.'
            elif player.decision == 'Steal' and self.num_cooperators == 0:
                player.delta_energy_level = random_energy_cost + Constants.lone_payoff
                player.outcome = 'You tried to steal but there was no-one cooperating to steal from.'
                        
        for player in players:
            player.mock_payoff = player.participant.payoff + player.delta_energy_level 
class Player(BasePlayer):
    decision = models.StringField(choices=[['Work alone', 'Work alone'], ['Cooperate', 'Cooperate'], ['Steal', 'Steal']], widget=widgets.RadioSelect)
    outcome = models.LongStringField()
    energy_level = models.CurrencyField()
    delta_energy_level = models.CurrencyField()
    mock_payoff = models.CurrencyField()
    Payoff = models.CurrencyField(initial=100)