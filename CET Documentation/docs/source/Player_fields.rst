.. raw:: pdf

    PageBreak

Player Class
=================

Here's an overview of all fields and functions in the Player class:

Fields
---------

.. _carbon_ref:

Carbon
~~~~~~~~~~~~~~~~~~~~~~~~
 - The ``player.carbon`` field specifies the  carbon value in lbs for each round of the CET.

.. _car_miles_ref:

Car Miles
~~~~~~~~~~~~~~~~~~~~~~
 - ``player.car_miles`` field specifies the equivalent of the carbon value in miles driven in a standard car.
 - This value serves as a real-life example for the players to understand the carbon footprint of the decision.

.. _bonus_ref:

Bonus
~~~~~~~~~~~~~~~~~~~~~~
 - ``player.bonus`` is a Currency field that specifies the monetary compensation a player receives,
   if the environmentally unfriendly Option A is picked.

The ``player.carbon``, ``player.car_miles`` and ``player.bonus`` value are initialised for all rounds before the start
of the experiment. See :ref:`creating_session_ref`

Decided
~~~~~~~~~~~~~~~~~~
 - ``player.decided`` is a Boolean field that states whether a player has made an autonomous decision or not.
 - ``True``: The player has decided on his/her own.
 - ``False``: A timeout happened.
 - A player has a ``decided`` value in each round of the CET.

.. _choice_ref:

Choice
~~~~~~~~~~~~~~~~~~~~~~
 - ``player.choice`` specifies the choice of the player for each round.
 - ``0``: Option B: The player decides to forfeit the bonus (Environmentally friendly decision).
 - ``1``: Option A: The player decides to take the bonus (Environmentally unfriendly decision).

Choice Practice
~~~~~~~~~~~~~~~~
 - ``player.choice_practice`` is needed to produce an error if player tries to click through practice rounds.
 - This field serves no other purpose and can be disregarded in the :ref:`export_ref`.

Total Emission
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
 - ``player.total_emission`` is the sum of the ``player.carbon`` values over all rounds the player has progressed so far.
 - This value increases every time a player progresses to a new round.
 - This field can be split into two sub_fields: ``player.chosen_emission`` and ``player.saved_emission``.

Chosen Emission
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
 - ``player.chosen_emission`` is the sum of all carbon values if Option A was clicked.
 - This value increases everytime the player chooses Option A.

Saved Emission
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
 - ``player.saved_emission`` is the sum of all carbon values if Option B was clicked.
 - This value increases everytime the player chooses Option B.

Is Bot
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
 - ``player.is_bot`` is a Boolean field that states if the player is seen as a Bot or not.
 - A player is regarded as a bot if the amount of autonomous decisions falls below the :ref:`bot_criteria_ref`.
 - The bot status of a player can vary from round to round depending on the player's percentage of autonomous decisions.

.. _is_dropout_ref:

Is Dropout
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
 - ``player.is_dropout`` is a Boolean field that states if the player is considered a dropout.
 - A dropout player is a player that mathematically cannot become "human" again.
 - **Example:**
   The CET has a total of 40 rounds. Let's assume the Bot Criteria is 0.75 so the player
   has to decide autonomously in 75% of all rounds. Hence, the player must make a decision in 30 of the total 40 rounds.
   So the player can miss a total of 10 rounds and can still avoid being considered a bot if he makes a decision in
   the remaining 30 rounds. However, once the player misses a total of 11 rounds, then the player can mathematically
   not become "human" again. As soon as this happens the ``player.is_dropout`` field turns ``True`` and the player is
   considered a dropout.
 - If the player is considered a dropout, then the :ref:`timeout_ref` for every remaining page is set to 0 seconds.
   Thus, the dropout player is automatically progressed through each round until the CET is finished.
   This drastically reduces the total experiment time, since experimenters don't have to wait on dropout players.
   This is espacially important because every player (also dropouts) have to finish the CET so the
   ``send_payment_mail()`` function is triggered. See :ref:`mail_call_ref`

Is Finished
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
 - ``player.is_finished`` is a Boolean field that states if the player has finished the CET or not.
 - A player is considered finished when the "Next" button on the Results page is pressed. See :ref:`results`

Payoff per Round
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
 - The ``player.payoff_per_round`` field contains the player's (hypothetical) payoff for each round.
 - If the player chooses environmentally-friendly Option B, the payoff is 0.
 - If the player chooses environmentally-unfriendly Option A, the payoff is ``player.bonus``.
 - ``player.payoff_per_round`` is used as a helper field and does NOT define the actual ``player.payoff`` field.
   The actual payoff is calculated in :ref:`set_payoff_ref`.

Functions
-------------

Current Question
~~~~~~~~~~~~~~~~~~~~~~~~
 - ``current_question`` is used to help initialize ``player.carbon``, ``player.car_miles`` and ``player.bonus``.
 - This function is called in :ref:`creating_session_ref`.

Set Total Emission
~~~~~~~~~~~~~~~~~~~~~~~~~~
 - ``set_total_emission`` sets the ``player.total_emission`` field.
 - This function is called in every round of the CET. See :ref:`exp_page`

Set Chosen Emission
~~~~~~~~~~~~~~~~~~~~~~~~~~
 - ``set_chosen_emission`` sets the ``player.chosen_emission`` field.
 - This function is called in every round of the CET. See :ref:`exp_page`

Set Saved Emission
~~~~~~~~~~~~~~~~~~~~~~~~~~
 - ``set_saved_emission`` sets the ``player.saved_emission`` field.
 - This function is called in every round of the CET. See :ref:`exp_page`

Set is Bot
~~~~~~~~~~~~~~~~~~~~
 - ``set_is_bot`` sets the ``player.is_bot`` and the ``player.is_dropout`` field.
 - This function is called in every round of the CET. See :ref:`exp_page`

Set Payoff per Round
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
 - ``set_payoffs_per_round`` sets the ``player.payoff_per_round`` field.
 - This function is called in every round of the CET. See :ref:`exp_page`

.. _set_payoff_ref:

Set Payoff
~~~~~~~~~~~~~~~~~~
 - ``set_payoff`` sets the ``player.payoff`` field.
 - The payoff is a built-in player field that does not have to be initialised and is used to determine the player's payoff.
 - This function is dependent on the :ref:`random_payoff` constant.
 - If ``random_payoff = True`` then the ``player.payoff`` = ``player.payoff_per_round`` in the paying round and 0 in every other round.
 - Else ``player.payoff`` = ``player.payoff_per_round`` for every round.
 - This function is called in every round of the CET.




