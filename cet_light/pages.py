from otree.api import Currency as c, currency_range
from ._builtin import Page, WaitPage
from .models import Constants


class Instruction_page(Page):
    def is_displayed(self):
        return self.round_number == 1

    timeout_seconds = 120  # Timeout needed for dropout players


class Practice_page_1(Page):
    def is_displayed(self):
        return self.round_number == 1

    form_model = 'player'
    form_fields = ['choice_practice']
    timeout_seconds = 20  # NOEL CHANGE

    def vars_for_template(self):
        return dict(
            practice1_carbon=0.23,
            practice1_carmiles=0.37,
            practice1_bonus=0.2
        )


class Practice_page_2(Page):
    def is_displayed(self):
        return self.round_number == 1

    form_model = 'player'
    form_fields = ['choice_practice']
    timeout_seconds = 20  # NOEL CHANGE

    def vars_for_template(self):
        return dict(
            practice2_carbon=4.46,
            practice2_carmiles=7.24,
            practice2_bonus=0.6
        )


class Practice_page_3(Page):
    def is_displayed(self):
        return self.round_number == 1

    form_model = 'player'
    form_fields = ['choice_practice']
    timeout_seconds = 20  # NOEL CHANGE

    def vars_for_template(self):
        return dict(
            practice3_carbon=19.85,
            practice3_carmiles=32.22,
            practice3_bonus=1
        )


class Experiment_page(Page):
    form_model = 'player'
    form_fields = ['choice']

    def get_timeout_seconds(self):
        # The get_timeout_seconds method is called BEFORE the before_next_page method.
        # So the player object here is always one round ahead and the is_dropout calculations
        # are not done properly. This fixes the problem. DO NOT REMOVE THIS BLOCK
        if self.player.round_number > 1:
            player = self.player.in_round(self.round_number - 1)
        else:
            player = self.player

        # Actual Timeout logic:
        if player.is_dropout:
            return 0
        else:
            return 20

    # The order must be kept like this so that everything is calculated properly.
    # Do not change the order unless you know what you are doing.
    def before_next_page(self):
        # Timeout check
        if self.timeout_happened:
            self.player.decided = False
            self.player.choice = 0
        else:
            self.player.decided = True

        # Payoff functions:
        self.player.set_payoff_per_round()
        self.player.set_payoff()

        # Emission functions
        self.player.set_chosen_emission()
        self.player.set_total_emission()
        self.player.set_saved_emission()

        # Bot check
        self.player.set_is_bot()

        # Last round check
        if self.round_number == Constants.num_rounds:
            self.subsession.set_sum_saved_emission()

        # Helpful prints
        self.subsession.helpful_prints()


class Results(Page):
    def is_displayed(self):
        return self.round_number == Constants.num_rounds

    def get_timeout_seconds(self):
        if self.player.is_dropout:
            return 0
        else:
            return 60

    # Show the payoff in the paying round on the results page
    def vars_for_template(self):
        return dict(
            payoff_in_paying_round=self.player.in_round(self.subsession.paying_round).payoff,
            choice_in_paying_round=self.player.in_round(self.subsession.paying_round).choice
        )

    def before_next_page(self):
        # Is finished fields and functions
        self.player.is_finished = True
        self.subsession.set_all_players_finished()  # Updates if all players have finished the CET

        # Helpful prints
        self.subsession.helpful_prints()

        # All finished check and send mail
        if self.subsession.all_players_finished:
            self.subsession.send_payment_mail(self.subsession.sum_saved_emission,
                                              "lbs",
                                              "Carbon Emission Task",
                                              "John Doe",
                                              "noel.strahm@students.unibe.ch")


page_sequence = [Instruction_page,
                 Practice_page_1,
                 Practice_page_2,
                 Practice_page_3,
                 Experiment_page,
                 Results
                 ]
