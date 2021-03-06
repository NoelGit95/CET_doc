.. raw:: pdf

    PageBreak

.. _templates_ref:

Templates
===========

Overview of the general structure of all html templates for the CET.

Block Styles
-------------

.. code-block:: django

    {% block styles %}
    ...
    {% endblock %}

In this section you can define graphical options for the elements displayed in :ref:`block_content_ref`.

Error message
~~~~~~~~~~~~~~

.. code-block:: css

    .otree-form-errors {
    visibility: hidden;
    display: none;
    }

``visibility: hidden`` hides a possible error message, but the element will still take up space on the page.
In contrast, ``display: none`` completely removes the element.
It is possible to show a different error message should participants fail to choose
one of the necessary options to advance (e.g., one of the two options in the CET). The message can be modified
within the ``{% block content %}`` inside this block:

.. code-block:: django

    {% if form.errors  %}
    <div class="alert alert-danger" role="alert">
        <p>Please choose one of the required fields.</p>
    </div>
    {% endif %}

The expression ``{{ form.choice.errors }}`` is inserted in both lines in
``{% block content %}`` which define the radio buttons to be displayed on the page. See :ref:`radio_ref`


Timer
~~~~~~~~

This section also includes options to apply and, if necessary, show the timer indicating the remaining
time on a given page. If a timeout is defined (on the page class), the display property can be specified
under ``.otree-timer`` (e.g., “none” or “block”; click `here <https://www.w3schools.com/cssref/pr_class_display.asp>`_
for more information). Furthermore, it is possible to specify that the timer only appears if a certain
amount of seconds remains before the next page is automatically displayed. Change the number in
``if (event.offset.totalSeconds === 10)`` according to your preferences.

The remaining code in the block style section is about graphical specifications (see information on “class” below).

.. _block_content_ref:

Block Content
----------------

.. code-block:: django

    {% block content %}
    ...
    {% endblock %}

In this section, you define what is to be displayed to the user. The Section is split into two
container classes. The Container for Option A and the Container for Option B. Further customizations of
the two containers can be done here.

.. _radio_ref:

Radio buttons
~~~~~~~~~~~~~~~~

.. code-block:: html

    <input type="radio" id="Option A" name="choice" value="1"> {{ form.choice.errors }}

This defines the radio button which is linked to the player's :ref:`choice_ref` field. The ``value`` defines what
is saved in the data if this button is chosen. The ``id`` attribute only serves as clarification in this case
to explicitly show which value is chosen for which option above, since the code is somewhat difficult
to oversee at first glance. (Generally, it could be styled in a similar way like the “class” attributes.)

