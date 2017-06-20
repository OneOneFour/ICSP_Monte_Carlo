Interfaces
===============

.. automodule:: sgc.widgets._interface
    :members:
    :undoc-members:
    :show-inheritance:

:mod:`text`
++++++++++++++++++++++++++

.. automodule:: sgc.widgets._interface.text

    .. autoclass:: SelectableText
        :members:
        :private-members:
        :show-inheritance:

        .. autoattribute:: _text

            The current text. For normal selectable text, this should be a
            string. For editable text, this should be a list containing each
            different character as a separate item.

        .. autoattribute:: _text_offset

            The offset in pixels from the left side of the widget's rect to the
            left edge of the text.

        .. autoattribute:: _text_pos

            Should always be initially set to _text_offset. Used internally.

        .. autoattribute:: _blink

            True if the cursor should be drawn this frame.

        .. autoattribute:: _select

            Index of starting position for current selection. None if no
            current selection. Combined with `_cursor_pos` defines the
            selection. Use `_select_fix()` if you need the current selection
            area.

        .. autoattribute:: _chars

            Tuple containing (pos, width) tuples representing the position
            and size of each character when rendered. Automatically generated
            by `_calc_chars()`.
