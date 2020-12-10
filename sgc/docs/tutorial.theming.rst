Theming
-------

This tutorial will show you how to theme the toolkit to better suit your game.

In the :py:mod:`Simple<sgc.widgets.base_widget>` widget's documentation, it
shows that the first argument of a widget can be used to change what's drawn.

Earlier, we created a button using this code:

.. literalinclude:: ../example/helloworld.py
   :lines: 14

This ignores the first argument and thus creates a default button.

Custom sizes
++++++++++++

We can change the size of the widget by specifying the size as the first
argument to the widget. This argument should be a tuple or list containing
the width and height:

.. code-block:: python

    btn = sgc.Button((20, 70), label="Clicky", pos=(100, 100))

This creates the button with a width of 20 pixels and height of 70 pixels.

Custom images
+++++++++++++

There are 2 ways to use custom images to make a widget fit into the design
of a game.

Pygame surface
==============

The first method is to pass an existing Pygame Surface object as the first
argument. This could be loaded using the pygame.image module, a surface
you've drawn on with code or anything else resulting in a Pygame Surface:

.. code-block:: python

    surf = pygame.Surface((200, 100))
    ... draw some stuff on surf ...
    btn = sgc.Button(surf, label="Clicky", pos=(100, 100))

Load image from file
====================

The second method is to pass a string containing the file name of an image
that can be loaded:

.. code-block:: python

    btn = sgc.Button("btn.png", label="Clicky", pos=(100, 100))

.. note::

    This will load the image using pygame.image.load(surf).convert_alpha().
    If you want to load the image differently, then load it manually and
    pass the resulting surface in as shown in the previous sub-section.

Using multiple images
+++++++++++++++++++++

If you look at the documentation for some widgets, such as the
:py:class:`Button<sgc.widgets.button.Button>` widget, you will find some
list multiple images which can be used for different states. The Button
lists 3 images: 'image', 'over' and 'down'. These represent different states
of the button and each can use a different image.

In order to use images for these different states, we must pass in a dictionary;
the keys should be strings matching the image states, while the values should
be either a string or Pygame Surface in the same manner as the previous section:

.. code-block:: python

    imgs = {"image": "off.png", "over": "over.png", "down": "down.png"}
    btn = sgc.Button(imgs, label="Clicky", pos=(100, 100))
