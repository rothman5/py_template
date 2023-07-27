"""Custom value entry widget.

Author: Rasheed Othman
Created: July 26, 2023
"""

import tkinter as tk
from tkinter import ttk
from frames import RootFrame
from .label_text import LabelText


class ValueEntry(tk.Frame):
    """Value entry widget class."""

    def __init__(
        self, parent: type[RootFrame], text: str, default: int, domain: tuple[int, int]
    ) -> None:
        super().__init__(master=parent)

        self.domain = domain
        self.default_value = default

        self.value = tk.StringVar(value=f"{default:,}")

        self.entry_label = LabelText(self, text, ("#000000", "w", "left", False))

        self.entry = ttk.Entry(
            master=self, textvariable=self.value, justify="center", width=10
        )

        self.grid_columnconfigure(index=1, weight=1)

        self.entry_label.grid(row=0, column=0, sticky="nsew")
        self.entry.grid(row=0, column=2, sticky="nsew")

    def get_value(self, error_label: LabelText) -> int:
        """Get the entry's current value.

        Args:
            error_label (LabelText): The calling frames associated error label text frame.

        Returns:
            int: The entry's current value (-1 for non integers)
        """
        try:
            value = self.value.get()
            if value < self.domain[0]:
                msg = f"Error: Enter an integer greater than {self.domain[0]}."
                error_label.set_text(msg, "#ff3333", 3000)
                return -1

            if value > self.domain[1]:
                msg = f"Error: Enter an integer less than {self.domain[1]}."
                error_label.set_text(msg, "#ff3333", 3000)
                return -1

            return value

        except tk.TclError:
            error_label.set_text("Error: Entry must be an integer.", "#ff3333", 3000)
            return -1

    def set_value(self, value: int) -> None:
        """Set the entry's value as a formatted integer.

        Args:
            value (int): Value to set on the entry.
        """

        self.value.set(value=f"{value:,}")
