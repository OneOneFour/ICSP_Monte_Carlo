Getting Started
---------------

Here is a simple example of using the SGC toolkit.
It is described in more detail below.

.. literalinclude:: ../example/helloworld.py
    :language: python
    :linenos:
    :emphasize-lines: 1-2,10,14-15,21,26

The file is available as ``example/helloworld.py`` in the 
source distribution.

Breakdown
+++++++++

.. literalinclude:: ../example/helloworld.py
   :lines: 1-2

Here we import everything we need from sgc.

----------

.. literalinclude:: ../example/helloworld.py
   :lines: 4-8

The toolkit needs to have the display and font modules initialised;
``pygame.init()`` would suffice.

----------

.. literalinclude:: ../example/helloworld.py
   :lines: 10

This creates a screen object, in much the same way as 
``pygame.display.set_mode()`` does. This is required for the toolkit to
function.

----------

.. literalinclude:: ../example/helloworld.py
   :lines: 14-15


This creates a new button widget, setting the label to 'Clicky' and the top-left
position of the widget to (100,100). The other line adds the button to the
screen, with the `0` specifying the focus order of the widget,
meaning the button will be the first widget to be focused
when the user hits the :kbd:`TAB` key.

----------

.. literalinclude:: ../example/helloworld.py
   :lines: 21

This function sends an event through to the toolkit. This function should
appear in your event loop in order to handle all incoming events.

----------

.. literalinclude:: ../example/helloworld.py
   :lines: 26

This function should be called on each frame before the screen is updated.
It should be given the time passed since the last frame; this is usually
obtained from ``clock.tick()``.
