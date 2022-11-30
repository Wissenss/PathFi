import tkinter as tk
from tkinter import ttk

from theme import DarkBlue

DARKBLUE = "#215d9c"

class MenuPage(tk.Frame):
    def __init__(self, container, controller):
        super().__init__(container)

        self.controller = controller

        self.style = DarkBlue(self)

        menu = tk.Frame(self)
        menu.pack(expand=1)

        title = ttk.Label(menu, text="PathFi Lab", font=('Helvetica', 20, "bold"), foreground=DARKBLUE)
        title.pack()
        button = ttk.Button(menu, text="Sandbox", padding=(5,5,5,5), command=controller.renderSandboxPage)
        button.pack(pady=(30,0))
        button = ttk.Button(menu, text="Competitive", padding=(5,5,5,5), state=tk.DISABLED)
        button.pack(pady=(5,0)) 

    def configWindow(self):
        self.controller.geometry("400x250")
        self.controller.resizable(False, False)