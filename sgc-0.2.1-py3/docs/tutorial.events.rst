Events
------

This tutorial will show you how to utilise events.

All event methods are recognised by the naming convention of having *on_*
prepended to their names. You will find these methods documented within each
widget, for example the Button widget has an
:py:meth:`on_click()<sgc.widgets.button.Button.on_click>` method; this is run
whenever the button is clicked via mouse or keyboard.

Events
++++++

The event methods, if left unchanged, will emit a Pygame event. All events use
the :py:mod:`GUI<sgc.locals>` constant for their type attribute.


Try adding this code to the event loop of your program or the getting started
code to see all the events being emitted by the toolkit:

.. code-block:: python

    if event.type == GUI:
        print event

All of these events also have these extra attributes:

.. py:attribute:: widget_type

    The class of the widget that emitted the event.

.. py:attribute:: widget

    The instance of the widget that emitted the event.

.. py:attribute:: gui_type

    A string indicating what this event represents.

Some events will have additional attributes and are documented with their
event methods.

Callbacks
+++++++++

If you prefer to use callbacks rather than handling events, this can be
easily accomplished by overloading the method.

You could do this using a subclass:

.. code-block:: python

    class MyButton(sgc.Button):
        def on_click(self):
            print "Overloading through inheritance."

Or, you could simply reassign a function:

.. code-block:: python

    def foo():
        print "Replace through assignment."

    my_button.on_click = foo

Or, you can pass the function into
:py:meth:`config()<sgc.widgets.base_widget.Simple.config>` to assign it:

.. code-block:: python

    def foo():
        print "Assign through config."

    my_button.config(on_click=foo)

Using both events and callbacks
+++++++++++++++++++++++++++++++

Because using a callback will suppress the event, if you want to use both
callbacks and events for a widget you must call the original method in
your callback.

.. code-block:: python

    class MyButton(sgc.Button):
        def on_click(self):
            sgc.Button.on_click(self)
            print "Using a callback and sending an event."
