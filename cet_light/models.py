from otree.api import (
    models,
    widgets,
    BaseConstants,
    BaseSubsession,
    BaseGroup,
    BasePlayer,
    Currency as c,
    currency_range,
)
import random
import csv
import smtplib  # Noel Change
import requests  # Noel Change
import traceback # Noel Change


author = 'db'

doc = """
Carbon Emission Task
"""


class Constants(BaseConstants):
    name_in_url = 'cet_light'
    players_per_group = None

    # Import datafile
    with open('cet_light/cet_data.csv') as f:
        questions = list(csv.DictReader(f, quoting=csv.QUOTE_NONNUMERIC))

    # DEFINE YOUR CONSTANTS HERE
    #num_rounds = len(questions) #This is the actual one
    num_rounds = 3  # NOEL CHANGE
    random_payoff = True
    random_saved_emission = False
    Bot_criteria = 0.75



class Subsession(BaseSubsession):

    # SUBSESSION FIELDS:
    all_players_finished = models.BooleanField(initial=False)
    paying_round = models.IntegerField()
    sum_saved_emission = models.FloatField(initial=0)

    # SUBSESSION FUNCTIONS:
    def creating_session(self):
        # Define the paying round. This page gets executed "num rounds" times so only do this calculation once.
        if self.round_number == 1:
            self.paying_round = random.randint(1, Constants.num_rounds)
            print('Paying round is: ', self.paying_round)

            # Randomize the order of 'questions' for each player.
            for p in self.get_players():
                p.participant.vars['questions'] = random.sample(Constants.questions, len(Constants.questions))

        #Initialise the paying_round Field for all rounds.
        self.paying_round = self.in_round(1).paying_round

        #Initialise question data, carbon, bonus abd car mile values
        for p in self.get_players():
            question_data = p.current_question()
            p.carbon = question_data['carbon']
            p.bonus = question_data['bonus']
            p.car_miles = question_data['car_miles']


    def set_all_players_finished(self):
        sum_finished = 0
        for p in self.get_players():
            if p.is_finished:
                sum_finished += 1

        if sum_finished == self.session.num_participants:
            self.all_players_finished = True
        return sum_finished  # Only needed for the helpful_prints Function


    def set_sum_saved_emission(self):
        self.sum_saved_emission = 0
        for p in self.get_players():
            # Exclude bots
            if p.in_round(Constants.num_rounds).is_bot == False:
                # Different calculations based on random_saved_emission
                if Constants.random_saved_emission == True:
                    if p.in_round(self.paying_round).choice == 0:
                        self.sum_saved_emission += p.in_round(self.paying_round).carbon
                else:
                    self.sum_saved_emission += p.in_round(Constants.num_rounds).saved_emission

        self.sum_saved_emission = round(self.sum_saved_emission, 3)


    def helpful_prints(self):
        for p in self.get_players():
            print("\nPLAYER VARIABLES FOR PLAYER", p.id_in_group, "IN ROUND", p.round_number)
            print("Total saved emission:", p.saved_emission)
            print("Total Carbon Chosen:", p.chosen_emission)
            print("The player is currently evaluated as a bot:", p.is_bot)
            print("The player is currently evaluated as a dropout:", p.is_dropout)
            print("This is the payoff_per_round variable in this round: ", p.payoff_per_round)
            if self.round_number == self.paying_round and Constants.random_payoff == True:
                print("This is the Paying round. The players payoff is: ", p.payoff)

        print("\nSUBSESSION VARIABLES:")
        print("Random saved_emission:", Constants.random_saved_emission, "; Sum saved emission (no bots): ", self.in_round(Constants.num_rounds).sum_saved_emission)
        print("How many players have finished the CET:", self.in_round(Constants.num_rounds).set_all_players_finished(), "of", self.session.num_participants, "have finished\n")


    def send_payment_mail(self,
                          weight_to_donate: float,
                          unit: str = "t",
                          experiment_name: str = "Carbon Emission Task",
                          payment_e_mail_name: str = "John Doe",
                          payment_e_mail_to: list = ["noel.strahm@students.unibe.ch"]):

        #CONSTANTS:
        MAIL_USER = "d0d337e96041c7f2d952902f72af6557"
        MAIL_PASS = "dc40f2b5a87c4c983b92a8ca8cfd674c"
        MAIL_SERVER = "in-v3.mailjet.com"
        MAIL_SENDER = "noel.strahm@iop.unibe.ch"
        MAIL_PORT = 465
        DONATION_MINIMUM = 1    

        #Unit check: was a valid unit specified?
        unit_list = ["mg", "g", "kg", "t", "oz", "lbs", "st"]
        if unit not in unit_list:
            raise Exception("unit parameter ", unit, "not recognised. Unit has to be in ", unit_list)

        #Convert unit to metric tons.
        if unit == "mg":
            weight_in_tons = weight_to_donate / 1000000000
        if unit == "g":
            weight_in_tons = weight_to_donate / 1000000
        if unit == "kg":
            weight_in_tons = weight_to_donate / 1000
        if unit == "t":
            weight_in_tons = weight_to_donate
        if unit == "oz":
            weight_in_tons = weight_to_donate / 35273.96198069
        if unit == "lbs":
            weight_in_tons = weight_to_donate / 2204.62262185
        if unit == "st":
            weight_in_tons = weight_to_donate / 157.47304442

        #GETTING THE CURRENT CO2 PRICE:
        price = 0
        try:
            price = requests.get("http://compensate.compensators.org/price.php").json()
            if 'price_per_ton' not in price:
                raise Exception("Price not found in data")
            price_per_ton = float(price['price_per_ton'])
        except:
            pass
        donation_in_cents = weight_in_tons * price_per_ton

        # Check if Donation was smaller than 1 cent
        if donation_in_cents < DONATION_MINIMUM:
            print("The donation is less than 1 cent, therefore too small. No Mail was sent.")

        #SENDING THE PAYMENT MAIL
        else:

            #Define the body of the mail
            body = f"""Hello {payment_e_mail_name}, 
    
The participants in your experiment: "{experiment_name}" donated {weight_to_donate:.3f} {unit} of CO2 Emission. 
This equals to {weight_in_tons:.3f} tons of CO2. At the current price of {(price_per_ton / 100):.2f} € per ton this sums up to a total donation of {(donation_in_cents / 100):.2f} €. 
    
To authorize the payment, please click here: 
https://www.spendenformular-direkt.org/forms/6944d11a-60d9-48a2-803f-b4b0c7797cb9?default_amount_1_in_cents={donation_in_cents}
    
Best Regards
The Automated Donation system :)  
          """

            #Define the subject of the mail and add the mail body
            email_text = f"Subject: [{experiment_name}] Please confirm the donation for the experiment\n\n{body}"

            try:
                # Connect to the SMTP server.
                server = smtplib.SMTP_SSL(MAIL_SERVER, MAIL_PORT)

                #Login to the smtp server
                server.login(MAIL_USER, MAIL_PASS)

                # Send the email
                server.sendmail(MAIL_SENDER, payment_e_mail_to, email_text.encode('utf8', 'ignore'))
                server.close()
                print("Your mail has been sent successfully")

            except:
                print("Unable to send mail")
                traceback.print_exc()




class Group(BaseGroup):
    pass


class Player(BasePlayer):

    # PLAYER FIELDS:
    carbon = models.FloatField()
    car_miles = models.FloatField()
    bonus = models.CurrencyField()
    decided = models.BooleanField()
    choice = models.IntegerField()
    choice_practice = models.IntegerField()
    total_emission = models.FloatField()
    chosen_emission = models.FloatField(initial=0)
    saved_emission = models.FloatField(initial=0)
    is_bot = models.BooleanField(initial=False)
    is_dropout = models.BooleanField(initial=False)
    is_finished = models.BooleanField(initial=False)
    payoff_per_round = models.CurrencyField(initial=0)

    # PLAYER FUNCTIONS
    def current_question(self):
        return self.participant.vars['questions'][self.round_number - 1]


    def set_total_emission(self):
        for p in self.in_all_rounds():
            p.total_emission = round(sum([p.carbon for p in p.in_all_rounds()]), 3)


    def set_chosen_emission(self):
        for p in self.in_all_rounds():
            p.chosen_emission = round(sum([p.carbon for p in p.in_all_rounds() if p.choice == 1]), 3)


    def set_saved_emission(self):
        for p in self.in_all_rounds():
            p.saved_emission = round(p.total_emission - p.chosen_emission, 3)


    def set_is_bot(self):
        sum_decided = 0
        for p in self.in_all_rounds():
            # Bot calculation:
            sum_decided += p.decided

            if sum_decided / p.round_number < Constants.Bot_criteria:
                p.is_bot = True
            else:
                p.is_bot = False

            # Dropout calculation:
            max_possible = sum_decided + (Constants.num_rounds - p.round_number)
            if max_possible / Constants.num_rounds < Constants.Bot_criteria:
                p.is_dropout = True

    def set_payoff_per_round(self):
        for p in self.in_all_rounds():
            if p.choice == 1:
                p.payoff_per_round = p.bonus
            else:
                p.payoff_per_round = c(0)


    def set_payoff(self):
        if Constants.random_payoff == True:
            if self.round_number == self.subsession.paying_round:
                self.payoff = self.payoff_per_round
            else:
                self.payoff = c(0)
        else:
            self.payoff = self.payoff_per_round