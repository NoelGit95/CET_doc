.. raw:: pdf

    PageBreak

.. _cet_calculator:

Car Distance Calculator
==========================

The car_distance_calculator.xlsx file provides a usable calculator that determines how far an average UK car
can drive, given a certain amount of CO2 emission. The calculator can be used if experimenters decide to
choose a different weight unit other than pound to display the :ref:`carbon_ref` values
or use kilometers instead of miles to display the :ref:`car_miles_ref` values.

The calculator provides a C02 emission to car miles / kilometers conversion for the following weight units:
Milligrams (mg), Grams (g), Kilograms (kg), Tons (t), Pounds (lbs), Ounzes (oz) and Stones (st).
The weight of the CO2 emission is then converted to miles and kilometers driven in an average UK car
using petrol as fuel.

A more detailed description on how the calculator works is provided within the car_distance_calculator.xlsx file.

All carbon and car mile values must be changed in the :ref:`csv_file` in order to change the values during
the experiment.

Some further modifications to the CET can be made in the :ref:`constants` class of the models.py file.