"""Custom dropdown list widget.

Author: Rasheed Othman
Created: July 26, 2023
"""

import tkinter as tk
from tkinter import ttk
from frames import RootFrame
from .label_text import LabelText


class DropdownList(tk.Frame):
    """Dropdown list widget class."""

    def __init__(self, parent: type[RootFrame], text: str, callback: callable) -> None:
        super().__init__(master=parent)

        self.list_label = LabelText(self, text, ("#000000", "w", "center", False))

        self.dropdown_list = ttk.Combobox(master=self, state="readonly", width=10)
        self.dropdown_list.bind("<<ComboboxSelected>>", callback)

        self.grid_columnconfigure(index=1, weight=1)

        self.list_label.grid(row=0, column=0, sticky="nsew")
        self.dropdown_list.grid(row=0, column=2, sticky="nsew")

    def get_selection(self) -> str:
        """Get the dropdown list's currently selected value.

        Returns:
            str: Dropdown list selected value.
        """

        self.dropdown_list.master.focus_set()
        return self.dropdown_list.get()

    def set_list_values(self, values: list) -> None:
        """Set the dropdown list's values.

        Args:
            values (list): New values for the dropdown list.
        """

        values.insert(0, "None")
        self.dropdown_list["values"] = values
        if len(values) == 0:
            self.dropdown_list.set([])
