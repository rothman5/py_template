"""Custom label text widget.

Author: Rasheed Othman
Created: July 26, 2023
"""

import tkinter as tk
from tkinter import ttk
from frames import RootFrame


class LabelText(ttk.Label):
    """Label text widget class."""

    def __init__(
        self,
        parent: type[RootFrame],
        text: str,
        options: tuple[str, str, str, bool],
    ) -> None:
        super().__init__(
            master=parent,
            text=text,
            foreground=options[0],
            anchor=options[1],
            justify=options[2],
            wraplength=275,
        )

        self.default_text = text
        self.default_fg = options[0]

        self.label_text = tk.StringVar(value=text)

        self.config(textvariable=self.label_text)

        if not options[3]:
            self.separator = None
        else:
            self.separator = ttk.Separator(master=parent, orient="vertical")

    def set_default_text(self, text: str, foreground: str) -> None:
        """Set the default label text.

        Args:
            text (str): New default label text.
        """

        self.default_text = text
        self.default_fg = foreground
        self.set_text(text, foreground, -1)

    def get_text(self) -> str:
        """Get the label text.

        Returns:
            str: Current label text.
        """

        return self.label_text.get()

    def set_text(self, text: str, foreground: str, timeout: int) -> None:
        """Set the label text.

        Args:
            text (str): New label text.
            foreground (str): Label text font color.
            timeout (int): How long to display this text for (-1 for indefinite)
        """

        self.label_text.set(value=text)
        self.config(foreground=foreground)
        if timeout > 0:
            self.after(
                timeout, lambda: self.set_text(self.default_text, self.default_fg, -1)
            )
