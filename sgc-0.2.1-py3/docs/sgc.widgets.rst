widgets Package
===============

.. automodule:: sgc.widgets
    :members:
    :undoc-members:
    :show-inheritance:

Core Widgets
++++++++++++

:mod:`base_widget` Module
-------------------------

.. automodule:: sgc.widgets.base_widget
    :members:
    :undoc-members:
    :exclude-members: update, rect_abs, pos, pos_abs
    :show-inheritance:

:mod:`button` Module
--------------------

.. automodule:: sgc.widgets.button

    .. image:: images/button.png
       :alt: Button
       :align: right

    .. autoclass:: sgc.widgets.button.Button
        :members:
        :undoc-members:
        :show-inheritance:
        :exclude-members: update

        .. automethod:: config

:mod:`combo` Module
--------------------

.. automodule:: sgc.widgets.combo

    .. image:: images/combo.png
       :alt: Combo Box
       :align: right

    .. autoclass:: sgc.widgets.combo.Combo
        :members:
        :undoc-members:
        :show-inheritance:
        :exclude-members: update, selection

        .. automethod:: config

:mod:`fps_counter` Module
-------------------------

.. automodule:: sgc.widgets.fps_counter

    .. image:: images/fps_counter.png
       :alt: FPS Counter
       :align: right

    .. autoclass:: sgc.widgets.fps_counter.FPSCounter
        :members:
        :undoc-members:
        :show-inheritance:
        :exclude-members: update

        .. automethod:: config

:mod:`input_box` Module
-----------------------

.. automodule:: sgc.widgets.input_box

    .. image:: images/input_box.png
       :alt: Input Box
       :align: right

    .. autoclass:: sgc.widgets.input_box.InputBox
        :members:
        :undoc-members:
        :show-inheritance:
        :exclude-members: update, text

        .. automethod:: config

:mod:`label` Module
-------------------

.. automodule:: sgc.widgets.label

    .. image:: images/label.png
       :alt: Label
       :align: right

    .. autoclass:: sgc.widgets.label.Label
        :members:
        :undoc-members:
        :show-inheritance:
        :exclude-members: update, text

        .. automethod:: config

:mod:`menu` Module
------------------

.. automodule:: sgc.widgets.menu

    .. autoclass:: sgc.widgets.menu.Menu
        :members:
        :undoc-members:
        :show-inheritance:
        :exclude-members: update, func_dict

        .. automethod:: config

:mod:`radio_button` Module
--------------------------

.. automodule:: sgc.widgets.radio_button

    .. image:: images/radio_button.png
       :alt: Radio Button
       :align: right

    .. autoclass:: sgc.widgets.radio_button.Radio
        :members:
        :undoc-members:
        :show-inheritance:
        :exclude-members: update, groups, selected

        .. automethod:: config

:mod:`scale` Module
-------------------------

.. automodule:: sgc.widgets.scale

    .. image:: images/scale.png
       :alt: Scale
       :align: right

    .. autoclass:: sgc.widgets.scale.Scale
        :members:
        :undoc-members:
        :show-inheritance:
        :exclude-members: update, value

        .. automethod:: config

:mod:`settings` Module
----------------------

.. automodule:: sgc.widgets.settings
    :members:
    :undoc-members:
    :show-inheritance:

:mod:`switch` Module
-------------------------

.. automodule:: sgc.widgets.switch

    .. image:: images/switch.png
       :alt: Switch
       :align: right

    .. autoclass:: sgc.widgets.switch.Switch
        :members:
        :undoc-members:
        :show-inheritance:
        :exclude-members: update, state

        .. automethod:: config

Container Widgets
+++++++++++++++++

:mod:`container` Module
-----------------------

.. automodule:: sgc.widgets.container

    .. autoclass:: sgc.widgets.container.Container
        :members:
        :undoc-members:
        :show-inheritance:
        :exclude-members: update

        .. automethod:: config

:mod:`boxes` Module
-------------------

.. automodule:: sgc.widgets.boxes

    .. autoclass:: sgc.widgets.boxes.VBox
        :members:
        :undoc-members:
        :show-inheritance:
        :exclude-members: update

        .. automethod:: config

    .. autoclass:: sgc.widgets.boxes.HBox
        :members:
        :undoc-members:
        :show-inheritance:
        :exclude-members: update

        .. automethod:: config

:mod:`dialog` Module
--------------------

.. automodule:: sgc.widgets.dialog

    .. image:: images/dialog.png
       :alt: Dialog
       :align: right

    .. autoclass:: sgc.widgets.dialog.Dialog
        :members:
        :undoc-members:
        :show-inheritance:
        :exclude-members: update

        .. automethod:: config

:mod:`scroll_box` Module
------------------------

.. automodule:: sgc.widgets.scroll_box

    .. image:: images/scroll_box.png
       :alt: Scroll Box
       :align: right

    .. autoclass:: sgc.widgets.scroll_box.ScrollBox
        :members:
        :undoc-members:
        :show-inheritance:
        :exclude-members: update

        .. automethod:: config

Composite Widgets
+++++++++++++++++

:mod:`dialogs` Module
------------------------

.. automodule:: sgc.widgets.composite.dialogs

    .. image:: images/dialog_save_quit.png
       :alt: Save/Quit Dialog
       :align: right

    .. autoclass:: sgc.widgets.composite.dialogs.DialogSaveQuit
        :members:
        :undoc-members:
        :show-inheritance:
        :exclude-members: update

        .. automethod:: config
