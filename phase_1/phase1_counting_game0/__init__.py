from otree.api import *
import random

doc = """
Your app description
"""


class C(BaseConstants):
    NAME_IN_URL = 'phase1_counting_game0'
    PLAYERS_PER_GROUP = None
    NUM_ROUNDS = 1000
    payment_per_correct_answer = cu(0.25)


class Subsession(BaseSubsession):
    pass


class Group(BaseGroup):
    pass


class Player(BasePlayer):
    number_entered = models.IntegerField()
    sum_of_numbers = models.IntegerField()
    zeros_actual = models.IntegerField()
    ones = models.IntegerField()
    combined_payoff = models.CurrencyField()
    goal_set = models.BooleanField(initial=False)
    goal_set_amount = models.IntegerField(initial=0)
    goal_left = models.IntegerField(initial=0)
    goal_complete = models.BooleanField(initial=False)
    game_done = models.BooleanField(initial=False)
    answered = models.BooleanField(initial=False)
    correct_answer = models.BooleanField(initial=False)


# FUNCTIONS
def table_creation(player: Player) -> [str, int, int]:
    row, col, randomizer = 10, 15, random.randint(0, 100000)
    zeros, ones = 0, 0
    matrix = ''

    for i in range(row):
        for j in range(col):
            if random.randint(0, 100000) < randomizer:
                matrix += '0'
                zeros += 1
            else:
                matrix += '1'
                ones += 1
        matrix += '\n'
    
    player.zeros_actual = zeros
    player.ones = ones
    return [matrix, zeros, ones]


def get_timeout_seconds(player: Player):
        participant = player.participant
        import time

        return participant.expiry - time.time()


# PAGES
class Start(Page):
    @staticmethod
    def is_displayed(player):
        return player.round_number == 1
    

class SetGoal(Page):
    form_model = "player"
    form_fields = ["goal_set"]

    @staticmethod
    def is_displayed(player: Player):
        return player.round_number == 1

    @staticmethod
    def before_next_page(player: Player, timeout_happened):
        participant = player.participant
        import time

        participant.expiry = time.time() + 1*60 # change 0.5 back to ten

        if player.goal_set == True:
            player.goal_set_amount = 10
            player.goal_left = 10
            player.goal_complete = False

            participant.goal_set = player.goal_set
            participant.goal_set_amount = player.goal_set_amount
            participant.goal_left = player.goal_left
            participant.goal_complete = player.goal_complete
            print("GOAL SET!!!")
            print(participant.goal_set)
            print(participant.goal_set_amount)
            print(participant.goal_left)
            print(participant.goal_complete)
        else:
            print("there is no goal set. do you understand there is no goal set okay")
            player.goal_set = False
            player.goal_complete = False

            participant.goal_set = player.goal_set
            participant.goal_complete = player.goal_complete
            print(participant.goal_set)
            print(participant.goal_complete)


class AddNumbers(Page):
    form_model = "player"
    form_fields = ["number_entered"]
    timer_text = "Time left in counting game:"
    get_timeout_seconds = get_timeout_seconds

    @staticmethod
    def is_displayed(player: Player):
        return get_timeout_seconds(player) > 0 and player.goal_complete == False and player.game_done == False
    
    @staticmethod
    def vars_for_template(player: Player):
        participant = player.participant
        the_matrix_and_zeros = table_creation(player)
        matrix_and_zeros = [the_matrix_and_zeros[i] for i in range(len(the_matrix_and_zeros))]
        matrix_table = matrix_and_zeros[0]
        num_zeros = matrix_and_zeros[1] # REMOVE this before running the experiment!
        #print("participant goal set: ", participant.goal_set)
        player.goal_set = participant.goal_set
        print("player goal set: ", player.goal_set)
        print("participant goal complete: ", participant.goal_complete)
        player.goal_complete = participant.goal_complete
        print("player goal complete: ", player.goal_complete)
        if player.goal_set == True and player.goal_complete == False:
            player.goal_left = participant.goal_left
            print("goal left: ", player.goal_left)
            player.goal_set = participant.goal_set
            print("goal set:", player.goal_set)
            if player.goal_left > 0 and player.goal_set == True:
                goal = participant.goal_left
                return {
                    "matrix_table": matrix_table,
                    "goal": goal,
                    "num_zeros": num_zeros # REMOVE this before running experiment! We don't want them to know how many zeros there are in the table
                }
            else:
                return {
                    "matrix_table": matrix_table,
                    "num_zeros": num_zeros # REMOVE this before running experiment! We don't want them to know how many zeros there are in the table
                }
        else:
            return {
                "matrix_table": matrix_table,
                    "num_zeros": num_zeros # REMOVE this before running experiment! We don't want them to know how many zeros there are in the table
            }
    
    @staticmethod
    def before_next_page(player: Player, timeout_happened):
        participant = player.participant
        player.answered = True
        participant.answered = player.answered
        if player.zeros_actual == player.number_entered:
            player.payoff += C.payment_per_correct_answer
            player.goal_left -= 1
            participant.goal_left = player.goal_left
            print("participant goal left: ", participant.goal_left)
            player.correct_answer = True
            participant.correct_answer = player.correct_answer
            print("participant correct answer: ", participant.correct_answer)
            if player.goal_left <= 0 and player.goal_set == True:
                print("goal is complete!")
                player.goal_complete = True
                participant.goal_complete = player.goal_complete
            else:
                return
        else:
            player.correct_answer = False
            participant.correct_answer = player.correct_answer
            print("participant correct answer: ", participant.correct_answer)


class GoalMet(Page):
    form_model = "player"
    form_fields = ["game_done"]

    @staticmethod
    def is_displayed(player: Player):
        return player.goal_set == True and player.goal_complete == True
    
    @staticmethod
    def vars_for_template(player: Player):
        participant = player.participant
        return {
            "goal_set_amount": participant.goal_set_amount
        }
    
    @staticmethod
    def before_next_page(player: Player, timeout_happened):
        participant = player.participant
        player.correct_answer = False
        player.answered = False
        participant.correct_answer = player.correct_answer
        participant.answered = player.answered
        if player.game_done == False:
            print("goal met but GAME NOT DONE")
            player.goal_set = False
            participant.goal_set = player.goal_set
            print("participant goal set: ", participant.goal_set)


class Results(Page):
    get_timeout_seconds = get_timeout_seconds

    @staticmethod
    def is_displayed(player: Player):
        participant = player.participant
        return participant.answered == True

    timer_text = "Time left in counting game:"
    @staticmethod
    def get_timeout_seconds(player: Player):
        participant = player.participant
        import time

        return participant.expiry - time.time()
    
    @staticmethod
    def vars_for_template(player: Player):
        if player.goal_left > 0 and player.goal_set == True:
            participant = player.participant
            goal = participant.goal_left
            return {
                "goal": goal
            }
        else:
            return
        
    @staticmethod
    def before_next_page(player: Player, timeout_happened):
        participant = player.participant
        player.correct_answer = False
        player.answered = False
        participant.correct_answer = player.correct_answer
        participant.answered = player.answered
        if player.game_done == False:
            print("the game is not over...")
            if player.goal_complete == True: # if a goal was already completed
                player.goal_set = False
                participant.goal_set = player.goal_set
                print("participant goal set: ", participant.goal_set)
            elif player.goal_set == False: # if a goal was never set
                player.goal_set = False
                participant.goal_set = player.goal_set
                print("participant goal set: ", participant.goal_set)
            else: # if the goal was set but not completed
                player.goal_set = True
                participant.goal_set = player.goal_set
                print("participant goal set: ", participant.goal_set)


class CombinedResults(Page):
    @staticmethod
    def is_displayed(player: Player):
        participant = player.participant
        return player.round_number == C.NUM_ROUNDS or participant.expiry <= 0 or player.game_done == True

    @staticmethod
    def vars_for_template(player: Player):
        all_players = player.in_all_rounds()
        player.combined_payoff = 0
        for temp_player in all_players:
            player.combined_payoff += temp_player.payoff
        return {
            "combined_payoff": player.combined_payoff
        }
    
    @staticmethod
    def before_next_page(player, timeout_happened):
        participant = player.participant

        participant.combined_payoff = player.combined_payoff
    
    @staticmethod
    def app_after_this_page(player, upcoming_apps):
        if player.game_done == True:
            return "phase1_counting_game1"

page_sequence = [Start, SetGoal, AddNumbers, GoalMet, Results, CombinedResults]
