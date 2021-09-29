.. raw:: pdf

    PageBreak

.. _subsession_fields:

Subsession Class
=================

Here's an overview of all fields and functions in the Subsession class:

.. _creating_session_ref:

creating_session()
----------------------

 - The ``paying_round`` is set as a random round between 1 and ``num_rounds``.
 - The order of questions is randomized for each player.
 - The player's :ref:`carbon_ref`, :ref:`car_miles_ref` and :ref:`bonus_ref` fields are initialized for all rounds.

.. _paying_round_ref:

Paying Round
----------------

 - The ``paying_round`` is the round where the player's payoff is calculated if ``random_payoff = True``. See :ref:`random_payoff`
 - A player's saved emission in the ``paying_round`` is added to the ``sum_saved_emission`` field if ``random_saved_emission = True``. See :ref:`random_emission`


.. _sum_saved_emission_ref:

Sum saved Emission
-------------------------------------------

Field
~~~~~~~~

 - The ``sum_saved_emission`` field is the sum of the ``saved_emission`` player field for all players.
 - The sum is either calculated across the ``paying_round`` or across all rounds depending on the :ref:`random_emission` field.
 - The field is used as an input in the :ref:`mail_ref` function.
 - Excludes all players that ar seen as bots. See :ref:`bot_criteria_ref`

Function
~~~~~~~~~~

 - The ``set_sum_saved_emission()`` function sets the ``sum_saved_emission`` field.
 - Checks if a player is a bot. See :ref:`bot_criteria_ref`
 - If a player is not a bot then the total ``saved_emission`` of all players is added to the ``sum_saved_emission``
   (Either across the paying round or all rounds).
 - A player has to finish all rounds of the CET, so that the correct data is available. Therefore, this function is only called in the last round of the CET. See :ref:`exp_page`


All Players Finished
----------------------

Field
~~~~~~
 - ``all_players_finished`` is a Boolean field that turns ``True`` once all players have finished the CET.


Function
~~~~~~~~~~
 - ``set_all_players_finished()`` calculates how many players in total have finished the CET (``sum_finished``).
 - If ``sum_finished`` = Number of participants then the ``all_players_finished`` field turns ``True``.
 - This function is only called once (for each player): When the player hits the "Next" button on the
   :ref:`results`.

Helpful prints
-------------------
 - The ``helpful_prints()`` function prints helpful information about the current state of many player and subsession fields to the terminal.
 - The function can be extended at will and be used for bug fixing purposes, if a new field is added.
 - The function is called in every round of the CET and when a player finishes the CET.
 - The function is only useful if the number of participants is small.

.. _mail_ref:

Send Payment Mail
--------------------

The ``send_payment_mail()`` function is used to automate carbon-emission certificate purchases for experiments with real-carbon externalities, such as the CET.
For more information see `ACO Documentation <https://aco-doc.readthedocs.io/en/latest/>`_.

Requirements
~~~~~~~~~~~~~~~~
 - The modules requests and smtplib have to be imported at the top of the models.py file.
 - A valid account from an SMTP service provider is needed. The credentials of the account have to be specified at
   the top of the function.

Parameters
~~~~~~~~~~~~~~
 - ``weight_to_donate``: A float value used to pass the amount of carbon emission that is saved by the experimental participants. The :ref:`sum_saved_emission_ref` is used for this.
 - ``unit``: A string value that defines the unit of the saved carbon emission. The following values are accepted: ``["mg", "g", "kg", "t", "oz", "lbs", "st"]``
 - ``experiment_name``: A string value that specifies the name of the experiment (e.g. "Carbon Emission Task")
 - ``payment_e_mail_name``: A string that specifies the name of the person or team that receives the mail
 - ``payment_e_mail_to``: A list containing the mail addresses of all recipients . If the mail is only to be sent to one address then a single string can be passed to the function.

How it works (basic)
~~~~~~~~~~~~~~~~~~~~~~~~
 1. The ``weight_to_donate`` value is converted to metric tons. The conversion is based on the ``unit`` value.
 2. The current CO2 price per ton for emission certificates is fetched from a price endpoint that is provided by
    `Compensators <https://www.compensators.org/>`_.
 3. The price of the carbon-emission certificate is calculated.
 4. A mail is sent to all addresses within the ``payment_e_mail_to`` list.
    The mail includes the total weight of carbon-emission saved,
    the current price per ton for carbon-emission certificates, as well as the link to Compensators
    `donation form <https://www.spendenformular-direkt.org/forms/6944d11a-60d9-48a2-803f-b4b0c7797cb9>`_
    with the correct price to make the carbon-emission certificate purchase.
    These contents can be changed at will.

.. _mail_call_ref:

When is send_payment_mail() called?
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
 - The function is called when all players have finished the CET. For an example see :ref:`results`


