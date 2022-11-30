import tkinter as tk
from tkinter import ttk

class CompetitivePage(tk.Frame):
    def __init__(self, container, controller):
        super().__init__(container)

        button = ttk.Button(self, text="test")
        button.pack()