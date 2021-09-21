.. raw:: pdf

    PageBreak

.. _constants:

Constants
=================

The following Constants can be set in the Constants class:


.. _random_payoff:

Random Payoff
---------------

 - ``random_payoff`` is used to define your preferred payoff calculation for the ``player.payoff`` field.
 - If set to ``True`` a player's payoff is only calculated in the ``paying_round``.
   The payoff in all other rounds is 0. See :ref:`paying_round_ref`
 - If set to ``False`` a player's payoff is calculated in all rounds.


.. _random_emission:

Random Saved Emission
-----------------------

 - ``random_saved_emission`` is used to define how the ``Subsession.sum_saved_emission`` field is calculated. See :ref:`sum_saved_emission_ref`
 - If set to ``True`` the sum is calculated by adding each player's saved emission in the ``paying_round``.
 - If set to ``False`` the saved emission for all rounds is added.

.. _bot_criteria_ref:

Bot Criteria
----------------

 - ``Bot_criteria`` is used to define the criteria as to when a player is seen as a bot.
 - ``Bot_criteria`` must be a value between 0-1 that represents the percentage of autonomous decisions a player has to make in order to be seen as human.
 - Example: The definition below means a player must decide autonomously (No timeout happened) in at least 75% of all rounds. Otherwise the player is regarded as a bot.

.. code-block:: python

    Bot_criteria = 0.75

Num Rounds
------------
 - This is an oTree specific variable that defines the number of rounds of the CET.
 - The number of rounds is defined as the length of the :ref:`csv_file` that contains the carbon data. If no changes
   are made this equals to 40 rounds.