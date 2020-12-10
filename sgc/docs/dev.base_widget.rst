Developer documentation
-----------------------

_locals
=======

.. automodule:: sgc.widgets._locals
    :members:
    :undoc-members:

Base widget
===========

.. automodule:: sgc.widgets.base_widget
    :undoc-members:
    :show-inheritance:

    .. class:: sgc.widgets.base_widget.Simple

        **Attributes to customise widget:**

        .. autoattribute:: _can_focus

            True if the widget can receive focus. The widget will not be able to
            receive events if it is not focused.

        .. autoattribute:: _default_size

            `(w,h)` A tuple containing the default size of the widget in pixels.

        .. autoattribute:: _modal

            True if the widget should be modal (blocks other widgets from
            receiving focus). This will normally be used in combination with
            `_layered`.

        .. autoattribute:: _layered

            True if the widget should be layered. This means the widget
            will float above other widgets, such as a dialog window.

        .. autoattribute:: _surf_flags

            Flags to be passed to `pygame.surface.Surface` when
            creating the images. This will typically just be `SRCALPHA` when
            the widget wants transparency.

        .. autoattribute:: _available_images

            This is a tuple containing the names of the different image
            states for the widget. See the :ref:`tutorial<available-images>`.

        .. autoattribute:: _extra_images

            This is a dictionary containing the names and sizes of the extra
            images for the widget. See the :ref:`tutorial<extra-images>`.

        .. autoattribute:: _image_state

            Change this attribute to change the default image state the widget
            should display. This should not be changed directly after
            initialisation.

        .. autoattribute:: _settings_default

            This is a dictionary containing the default settings for the
            widget. It will be copied to `self._settings` when the widget is
            instantiated.

        .. autoattribute:: _parent

            This should be assigned the parent widget, if this widget is
            attached to another. This is mainly used in container widgets.

        **Override these methods to customise widget behaviour:**

        .. automethod:: update

        .. automethod:: _event

        .. automethod:: _change_focus

        .. automethod:: _config

            Override to provide configuration options. Receives the keyword
            arguments user passed to `self.config()`. Will also receive "init"
            when the widget is instantiated, which can be used to initialise
            some things (preferred from overriding __init__).

        .. automethod:: _draw_base

        .. automethod:: _draw_final

        .. automethod:: _focus_enter

        .. automethod:: _focus_exit

        **Useful functions that can be used by the widget:**

        .. automethod:: _create_base_images

        .. automethod:: _dotted_rect

        .. automethod:: _create_event

        .. automethod:: _switch

    .. autoclass:: sgc.widgets.base_widget._Label

        .. autoattribute:: col

        .. autoattribute:: font

        .. autoattribute:: text

            The text that should be displayed. Changed in the base widget
            when "label" is passed to `self.config()`.

        .. autoattribute:: side

        .. autoattribute:: rect

        .. automethod:: _draw
