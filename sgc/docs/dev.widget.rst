Creating new widgets
--------------------

This page will show you what is required to create a new custom widget.

A first widget
++++++++++++++

A basic widget
==============

.. literalinclude:: ../example/custom_widget.py
    :linenos:
    :lines: 1-8

This widget is available in the example/custom_widget.py file.

The top lines here import some common things that will be needed in most
widgets.

Line 7 defines our new widget as `MyBasicWidget` and inherits
from :py:class:`Simple<sgc.widgets.base_widget.Simple>`. This is the base
widget that all widgets must inherit from.

Line 8 sets the default size of the widget when the user doesn't specify a size.

Using the widget
________________

This is our first widget complete. You can now use this widget in a program
using the typical code:

.. code-block:: python

    from custom_widget import MyBasicWidget
    widget = MyBasicWidget()
    widget.add()

If you use this code in your program, you should see a black square
representing the widget, as we haven't told it to draw anything more
interesting. It also has no interactivity and will simply sit there doing
nothing.

One thing you can see, is that a lot of the basic widget behaviour is
inherited. So, we can add and remove it like any other widget and it will fade
in and out. We can also use a custom size, change it's position and add a
label to this basic widget. All this functionality comes free from the base
widget.

.. code-block:: python

    widget = MyBasicWidget((200,100), pos=(10,200),
                           label="Free label", label_side="top")

Expanding on the widget
+++++++++++++++++++++++

We are now going to create a new widget called `MyWidget` with more features.
This widget is located in the same file as `MyBasicWidget`.

Settings
========

There is a convenience dictionary for storing configuration settings for each
widget.

.. literalinclude:: ../example/custom_widget.py
    :linenos:
    :lines: 15

We can put all the default setting values into `_settings_default` dictionary.
When the widget is instantiated this dictionary will be copied to `_settings`.
You can then use this dictionary to access and change the settings as we will
do later.

Drawing
=======

.. _available-images:

Regular images
______________

.. literalinclude:: ../example/custom_widget.py
    :linenos:
    :lines: 12

This class attribute lists all the different image states your widget will have.
It should be a tuple listing all the alternative states your widget should
draw. The default state is "image" and should not be listed. For example, a
button would have it's default off state, a state when the cursor hovers over
and another state when the user is clicking down on the button; so we would
use the tuple `("over", "down")` to give us those 3 images to work with.

These images will all be created at the widget's size.

Our widget will have an over state when the user hovers the mouse over it.

.. literalinclude:: ../example/custom_widget.py
    :linenos:
    :pyobject: MyWidget._draw_base

The `_draw_base()` function will draw our base images. Here we use a loop
through `self._available_images` which will have been modified to include
"image". All our images are stored in `self._images` and indexed using their
name. In this function, we have made our base images to be black with a red
or green circle.

This function will only be called when the user doesn't pass in a custom image.
If the user passes in a custom image, the widget will use that image instead.

.. literalinclude:: ../example/custom_widget.py
    :linenos:
    :pyobject: MyWidget._draw_final

The `_draw_final()` function works just like the previous `_draw_base()`
function. The only difference is that this function will be called at the end
of the drawing sequence, regardless of whether a custom image was passed in or
not. This should be used to draw something that should always appear, such as
the label on the `Button` widget.

In our function here, we are going to draw the text from our settings
dictionary onto the middle of the widget using the default "widget" font.

.. _extra-images:

Extra images
____________

Sometimes you want other images with your widget that are not the full size of
your widget.

.. literalinclude:: ../example/custom_widget.py
    :linenos:
    :lines: 13

The attribute `_extra_images` defines a dictionary containing these extra
images. The value for each image should be a tuple representing x and y size.
The x and y sizes should each be another tuple containing two numbers; the
first number is the ratio of the image to the widget size, while the second is
the number of pixels to offset from that size.

It is also possible to use an empty tuple as one of the sizes, in which case
the size will be copied from the other, allowing square images.

Our widget here, will have one extra image which is 30% of the widget's width
and 4 pixels shorter that the full height of the widget.

.. literalinclude:: ../example/custom_widget.py
    :linenos:
    :pyobject: MyWidget._draw_thing

For each extra image we have specified, we must supply an _draw_[`name`]()
method. This works much like the other draw functions, except that we only draw
on the one surface, and this surface is passed in as a 2nd argument,
along with the size of the image.

In this method we have filled our extra image with a random color.

Update
======

In order to give our widget some more dynamic behaviour, we can use the update
method.

.. literalinclude:: ../example/custom_widget.py
    :linenos:
    :pyobject: MyWidget.update

When the widget is on-screen, this method will be called every frame. It is
given the time passed since the last frame in milliseconds.

In this method we make the extra image of our widget move along the x axis to
align with our mouse.

Creating Events
===============

We can utilise events in our widget by defining an `on_[name]()` method. The
method must be prefixed with "on\_" to ensure the event can be set through the
config() method automatically and to ensure the :py:class:`sgc.locals.EventSlot` 
object will work.

.. literalinclude:: ../example/custom_widget.py
    :linenos:
    :pyobject: MyWidget.on_click

Our method should simply post an event. The event is created from the
:meth:`_create_event()<sgc.widgets.base_widget.Simple._create_event>`
method. The first argument must be the value of "gui_type" that should roughly
describe what will trigger the event. It also accepts optional keyword arguments
that define extra attributes for the event object.

This method defines an `on_click()` method for our widget. It will emit a
"click" event and give the on/off state as an extra attribute.

Handling Events
===============

Another thing we can do to make our widget more dynamic is to respond to events.

.. literalinclude:: ../example/custom_widget.py
    :linenos:
    :lines: 14

The first thing we need to do, is to change the _can_focus attribute to `True`
in order to be able to receive any events in our widget.

.. literalinclude:: ../example/custom_widget.py
    :linenos:
    :pyobject: MyWidget._event

The `_event()` method receives any events when the widget is focused.

This method switches between image states when the player left-clicks our
widget, and shows/hides the extra image when clicking with another button.

Configuration Options
=====================

Another thing we may want to do, is provide some extra configuration options
to the user of our widget. For this we define an `_config()` method, this will
automatically be called when the user calls the inherited `config()` method.

.. literalinclude:: ../example/custom_widget.py
    :linenos:
    :pyobject: MyWidget._config

The `_config()` method is passed all the keyword arguments from the user. In
this method you will need to check for your arguments and handle them
appropriately. The most common thing to do, is to simply copy the values into
the settings dictionary; in our widget here, we have created a simple loop
that does just that. You may however need to do more complex processing of an
argument or provide validation before saving it into the settings dictionary.

The "init" argument is given when the widget is first instantiated. This
allows you to run some code that only needs to be run once. This method will
set the `y` position of the extra image, which won't need to be changed later.

Our example also allows the user to change the text displayed in the middle of
the widget and the colour of the font used. This replaces the base widget's
behaviour, and we no longer get a label added to the side.

Dotted Rectangle
================

When a widget receives keyboard focus, a common thing is for that widget to
have a dotted rectangle around it. If the `_draw_rect` attribute is set to
`True`, the widget will automatically draw a dotted rect around it when the
image state is changed.

.. literalinclude:: ../example/custom_widget.py
    :linenos:
    :pyobject: MyWidget._focus_enter

.. literalinclude:: ../example/custom_widget.py
    :linenos:
    :pyobject: MyWidget._focus_exit

These methods set the widget to draw the dotted rect when it gains focus via
the keyboard (by pressing the `TAB` key), and to stop drawing it when focus is
lost.

Other things
============

There are other class attributes you may need to use, and other inherited
methods that may be useful. You can find these documented on the
:doc:`dev.base_widget`.

Advanced
++++++++

We will finish up with a couple of more advanced things you may want to
accomplish when creating complex widgets.

Dynamic Sizing
==============

You can create dynamically sized widgets, for example a container
widget which sets it's size to that of it's children. To do so, make sure you
do not change `_default_size`. Then, later in your widget when you know what
size to make it, you need to call
:meth:`self._create_base_images(size)<
sgc.widgets.base_widget.Simple._create_base_images>`,
with size being a `(width, height)` tuple.

Container widgets
=================

To create a container widget, you should normally start by inheriting from
:class:`sgc.Container<sgc.widgets.container.Container>`; this will sort
out the basics of handling multiple children widgets. To use the Container's
features you will probably want to call `Container._config()` from your custom
`_config()` method.
