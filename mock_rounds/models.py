
from otree.api import (
    models, widgets, BaseConstants, BaseSubsession, BaseGroup, BasePlayer,
    Currency as c, currency_range
)

doc = ''
class Constants(BaseConstants):
    name_in_url = 'mock_game'
    players_per_group = 2
    num_rounds = 20
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
        steal_success_prob = self.session.config["steal_success_prob"]
        cooperation_payoff = c(self.session.config["cooperation_payoff"])
        energy_cost = c(self.session.config["energy_cost"])
        energy_stochasticity = self.session.config["energy_stochasticity"]
        victims_payoff = c(self.session.config["victims_payoff"])
        steal_success_payoff = c(self.session.config["steal_success_payoff"])
        steal_failure_payoff = c(self.session.config["steal_failure_payoff"])
        lone_payoff = c(self.session.config["lone_payoff"])
        threshold = c(self.session.config["threshold"])
        penalty = self.session.config["penalty"]
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
            player.random_energy_cost = c(int(np.clip(np.random.normal(loc=energy_cost,scale=energy_stochasticity),-10,10).round()))
            if player.decision == 'Work alone':
                player.delta_energy_level = lone_payoff
                player.outcome = 'You worked alone.'
            elif player.decision == 'Cooperate' and self.num_cooperators < 2 and self.num_stealers == 0:
                player.delta_energy_level = lone_payoff
                player.outcome = ' You had to work alone'
            elif player.decision == 'Cooperate' and self.num_cooperators > 1 and self.num_stealers == 0:
                player.delta_energy_level = cooperation_payoff
                player.outcome = 'You cooperated successfully.'
            elif player.decision == 'Cooperate' and self.num_stealers > 0:
                if self.coin_toss < steal_success_prob:
                    player.delta_energy_level = -victims_payoff
                    player.outcome = 'You were stolen from.'
                elif self.num_cooperators < 2:
                    player.outcome = 'Someone tried to steal but you caught them. However, no-one else wanted to cooperate.'
                    player.delta_energy_level = lone_payoff
                else: 
                    player.delta_energy_level = cooperation_payoff
                    player.outcome = 'Someone tried to steal but you caught them.'
            elif player.decision == 'Steal' and self.num_cooperators > 0:
                if self.coin_toss < steal_success_prob:
                    player.delta_energy_level = steal_success_payoff
                    player.outcome = 'You stole successfully.'
                else: 
                    player.delta_energy_level = steal_failure_payoff
                    player.outcome = 'You tried to steal but got caught.'
            elif player.decision == 'Steal' and self.num_cooperators == 0:
                player.delta_energy_level = lone_payoff
                player.outcome = 'You tried to steal but there was no-one cooperating to steal from.'
                        
        for player in players: 
            if player.participant.vars['mocks_done']:
                player.participant.payoff = player.participant.payoff + player.delta_energy_level + player.random_energy_cost
                player.current_running = player.participant.payoff
                player.participant.vars['rounds_below_threshold'] += player.participant.payoff < threshold
            else:
                player.mock_payoff = player.participant.payoff + player.delta_energy_level + player.random_energy_cost
            player.rounds_below_threshold = player.participant.vars['rounds_below_threshold']
            player.virtual_cash_bonus = np.array(self.session.config['real_world_currency_per_point']*int(player.participant.payoff) - 
                self.session.config['penalty']*player.rounds_below_threshold).clip(0)
            player.delta_energy_level_absolute = np.abs(player.delta_energy_level)
            player.random_energy_cost_absolute = np.abs(player.random_energy_cost)
class Player(BasePlayer):
    decision = models.StringField(choices=[['Work alone', 'Work alone'], ['Cooperate', 'Cooperate'], ['Steal', 'Steal']], widget=widgets.RadioSelect)
    social_trust = models.IntegerField(choices=[[i,i] for i in range(11)], label = "How well do you trust the other members of your group to cooperate? (where 1 is not at all and 10 is totally)")
    outcome = models.LongStringField()
    energy_level = models.CurrencyField()
    delta_energy_level = models.CurrencyField(initial=0)
    delta_energy_level_absolute = models.CurrencyField(initial=0)
    random_energy_cost = models.CurrencyField(initial=0)
    random_energy_cost_absolute = models.CurrencyField(initial=0)
    mock_payoff = models.CurrencyField()
    rounds_below_threshold = models.IntegerField()
    virtual_cash_bonus = models.IntegerField()
    current_running = models.CurrencyField()
