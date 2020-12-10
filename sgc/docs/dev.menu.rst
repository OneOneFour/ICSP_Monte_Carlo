Menu Format
-----------

Here we are going to look at the format used for menu data.

.. note::

    At this time users will need to create this manually, but eventually there
    will be a menu creator that will allow creation of menus through a
    drag 'n' drop interface.

The menu format uses a fairly simple JSON format. We will look at the menu
created in the ``example/test.py`` program:

.. literalinclude:: ../example/menu
    :language: javascript
    :linenos:

The file is available as ``example/menu`` in the 
source distribution.

Breakdown
+++++++++

Menus
=====

.. literalinclude:: ../example/menu
   :lines: 1

The menu data must begin with an array at the top-level. The first item of this
array must be a string beginning with "m:", this signals the current item is a
menu. The rest of the string following the "m:" is the title to be displayed
at the top of this menu.

Each item in the array following is an item to be displayed in the menu.
Items will be displayed in the order they appear. So, this first array means the
menu has the title "Main Menu" and will display 3 items.

----------

.. literalinclude:: ../example/menu
   :lines: 2-6

The first item in the main menu, is another menu. This will display a sub-menu
when clicked from the main menu. The title "Sub-menu" will be displayed both as
the title when the menu is displayed, and also as the name of the item in it's
parent menu.

Again, this creates a menu with 3 items, which can be accessed from the
parent menu.

Widgets
=======

.. literalinclude:: ../example/menu
   :lines: 3

This line creates a widget to be displayed in the sub-menu. Like the menu, the
first item must be a string defining the object. It must begin with "w:" to
signal that this should be a widget. The text following the "w:" specifies the
widget type.

If you want to use one of the native widgets, then you must simply name the
widget using it's class name, such as "InputBox" or "Radio". If you want to
import a custom widget you must specify a full import path for the widget, such
as "foo.bar.CustomWidget".

The second item must be an object. This should contain the key:value options
to be passed into the widget to configure it's behaviour. Look at the widget's
config() method to see what arguments are accepted.

The "name" key is an extra key used by the menu. This key specifies a name
that the widget can be indexed by. The name used for this widget is "input", so
after using this file in a menu, I can use my_menu["input"] to access that input
box.

Dividers
========

.. literalinclude:: ../example/menu
   :lines: 4

An item which is just a string will be used a sub-title or divider. The contents
of the string will be used as the text for the divider. The resulting divider
will be a non-interactive object in the menu.

Tokens
======

.. literalinclude:: ../example/menu
   :lines: 5

This line creates another widget, this time a button. You'll notice one of the
arguments this time begins with a '$'. This is a token that tells the menu that
it refers to a function object. When the menu parses this text it will look in
the menu's :ref:`func-dict` for "print_input" and replace this string with the
found object.

If you want to create an object dynamically you can also add the syntax
to call a function. For example, `$foo("bar")` will call the function found
passing "bar" as an argument, the original string will then be replaced by
whatever is returned by this function.

----------

.. literalinclude:: ../example/menu
   :lines: 7-14

These lines creates a second sub-menu, containing two sub-menus itself, each
with a divider.

Functions
=========

.. literalinclude:: ../example/menu
   :lines: 15

This final item creates a function object. Again, the first item must be a
string, with the "f:" signalling that this is a function object. Following the
"f:" is the text that should be displayed in the menu. The second item is the
function that will be called when this item is clicked. This string will be
looked up in the menu's :ref:`func-dict` as before, though the '$' is
optional in this circumstance.

.. _func-dict:

Func dictionary
+++++++++++++++

When creating a menu using this format, you will need to specify a function
dictionary through inheritance. Here is the above example being used:

.. literalinclude:: ../example/test.py
   :lines: 44-51

As seen above, you must assign func_dict a lambda accepting the self argument.
This lambda must return a dictionary containing the token names as the keys,
and the actual functions as the values.

Doing this in code
++++++++++++++++++

This can also be all done in code, using lists and dictionaries instead of JSON.
You may also use tuples in place of lists. You can't use tokens if you choose
to do this in code, as you can pass in function objects directly.
