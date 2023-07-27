"""Custom checkbox widget.

Author: Rasheed Othman
Created: July 26, 2023
"""

import tkinter as tk
from tkinter import ttk
from frames import RootFrame


class Checkbox(tk.Frame):
    """Checkbox widget class."""

    def __init__(self, parent: type[RootFrame], text: str, state: bool) -> None:
        super().__init__(master=parent)

        self.check_state = tk.BooleanVar(value=state)
        self.check_button = ttk.Checkbutton(
            master=self,
            text=text,
            variable=self.check_state,
        )

        self.check_button.pack(side="top", anchor="center", fill="both", expand=True)

    def get_state(self) -> bool:
        """Return the checkbox state."""
        return self.check_state.get()
