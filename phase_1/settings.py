from os import environ

SESSION_CONFIGS = [
    dict(
      name="phase1",
      display_name="Phase 1",
      app_sequence=['phase1_counting_game0',
                    'phase1_counting_game1',
                    'phase1_counting_game2',
                    'payment_info'],
      num_demo_participants=4
    )
]

# if you set a property in SESSION_CONFIG_DEFAULTS, it will be inherited by all configs
# in SESSION_CONFIGS, except those that explicitly override it.
# the session config can be accessed from methods in your apps as self.session.config,
# e.g. self.session.config['participation_fee']

SESSION_CONFIG_DEFAULTS = dict(
    real_world_currency_per_point=1.00, participation_fee=0.00, doc=""
)

PARTICIPANT_FIELDS = ['expiry', 
                      'id_in_group', 
                      'combined_payoff', 
                      'standard', 
                      'wage_licensed', 
                      'wage_unlicensed', 
                      'licensed', 
                      'set_wage',
                      'goal_set',
                      'goal_set_amount',
                      'goal_left',
                      'goal_complete',
                      'goal_done',
                      'answered',
                      'correct_answer']
SESSION_FIELDS = []

# ISO-639 code
# for example: de, fr, ja, ko, zh-hans
LANGUAGE_CODE = 'en'

# e.g. EUR, GBP, CNY, JPY
REAL_WORLD_CURRENCY_CODE = 'USD'
USE_POINTS = False

ROOMS = [
    dict(
        name='econ101',
        display_name='Econ 101 class',
        participant_label_file='_rooms/econ101.txt',
    ),
    dict(name='live_demo', display_name='Room for live demo (no participant labels)'),
]

ADMIN_USERNAME = 'admin'
# for security, best to set admin password in an environment variable
ADMIN_PASSWORD = environ.get('OTREE_ADMIN_PASSWORD')

DEMO_PAGE_INTRO_HTML = """ """

SECRET_KEY = '7817700404848'
