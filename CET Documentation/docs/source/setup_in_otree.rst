.. raw:: pdf

    PageBreak

.. _setup_in_otree:

Set up the CET in oTree
==========================
This is how you import the Carbon Emission Task into your oTree framework.

Step 1: Download the CET
----------------------------
Download the CET folder from `Github <https://github.com/NoelGit95/CET_doc>`_

Step 2: Add the CET to your oTree Project
---------------------------------------------
Copy the CET folder into your oTree project directory like this:

--- Your_oTree_Project
    | - otree_app1
    | - otree_app2
    | ..
    | - cet_light
    | - manage.py
    | - requirements.txt
    | - settings.py

Step 3: Change session configurations in settings.py
-------------------------------------------------------
Include the CET app in your settings.py file. To do this append the following code in the
SESSION_CONFIGS list.

3.1: Dictionary
*****************

.. code-block:: python

    dict(
        name='cet_light',
        display_name="CET Light Version",
        num_demo_participants=40,
        app_sequence=['cet_light'],
    )


.. note::
    **Name Matching:** Like with any oTree app the specified name in the dict() must match the
    name of the project's folder. So make sure to change both the folder name as well as the
    ``name=''`` in the dict() in case you want to name the project any other way than *cet_light*.

3.2: Currency
****************

The :ref:`csv_file` provides the values for a player's bonus. The currency used is the Great British Pound. If you want
to use a different currency, the data in the cet_data file has to be adjusted accordingly. If no changes are made to
the cet_data file the currency parameters have to be specified as such:

.. code-block:: python

    # e.g. EUR, GBP, CNY, JPY
    REAL_WORLD_CURRENCY_CODE = 'GBP'
    USE_POINTS = False


Step 4: Install required packages
-------------------------------------

4.1: Download packages
*************************
The following packages that are not in the Python Standard Library are required:
`requests <https://pypi.org/project/requests/>`_

4.2: Add packages to requirements.txt
*****************************************
Add the following line to the ``requirements.txt`` file:

.. code-block:: python

    requests~=2.25.0 #Or higher version if this one is outdated.

