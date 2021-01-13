from os import environ
from fractions import Fraction
SESSION_CONFIG_DEFAULTS = dict(real_world_currency_per_point=3, participation_fee=0)
SESSION_CONFIGS = [dict(name='experiment', num_demo_participants=2,
	initial_mean_energy_level=105, initial_std_energy_level = 5,number_mock_rounds=3,r=0.1,mean_regression=True, 
	steal_success_prob = Fraction(1,3),victims_payoff=10,energy_stochasticity=3,energy_cost=0,
	cooperation_payoff=5,penalty=50,desperation=True,threshold=100,lone_payoff=0,steal_failure_payoff=-40,steal_success_payoff=20, 
	app_sequence=['instructions','mock_rounds','end_of_mock_rounds', 'real_rounds', 'debrief'])]
LANGUAGE_CODE = 'en'
REAL_WORLD_CURRENCY_CODE = 'USD'
USE_POINTS = True
DEMO_PAGE_INTRO_HTML = ''
ROOMS = [dict(name='dt_experiment', display_name='Experiment')]

ADMIN_USERNAME = 'admin'
# for security, best to set admin password in an environment variable
ADMIN_PASSWORD = environ.get('OTREE_ADMIN_PASSWORD')

SECRET_KEY = 'blahblah'

# if an app is included in SESSION_CONFIGS, you don't need to list it here
INSTALLED_APPS = ['otree']


