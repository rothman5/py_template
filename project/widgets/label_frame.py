"""Custom labeled frame.

Author: Rasheed Othman
Created: July 26, 2023
"""

from tkinter import ttk
from frames import RootFrame
from .label_text import LabelText


class LabeledFrame(ttk.Labelframe):
    """Labeled frame class."""

    def __init__(self, parent: type[RootFrame], label: str) -> None:
        super().__init__(master=parent, text=label)

        self.parent = parent

        self.top_frame = ttk.Frame(master=self)
        self.mid_frame = ttk.Frame(master=self)
        self.btm_frame = ttk.Frame(master=self)

        self.frame_text = LabelText(
            self.mid_frame, "", ("#4c566a", "center", "center", False)
        )

    def build_frame_sections(self) -> None:
        """Build the top, middle, and bottom sections of the custom frame."""

        if len(self.top_frame.winfo_children()) > 0:
            self.top_frame.pack(
                side="top", anchor="n", fill="both", expand=True, padx=(10, 10)
            )

        if len(self.mid_frame.winfo_children()) > 0:
            self.txt_label.pack(
                side="top",
                anchor="center",
                fill="both",
                expand=True,
                padx=(10, 10),
                pady=(0, 2),
            )
            self.mid_frame.pack(
                side="top", anchor="center", fill="both", expand=True, padx=(10, 10)
            )

        if len(self.btm_frame.winfo_children()) > 0:
            self.btm_frame.pack(
                side="bottom",
                anchor="s",
                fill="both",
                expand=True,
                padx=(10, 10),
                pady=(0, 10),
            )
