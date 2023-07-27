"""Application starting point.

Author: Rasheed Othman
Created: July 26, 2023
"""

from ctypes import windll

if __name__ == "__main__":

    windll.shcore.SetProcessDpiAwareness(1)
