import tkinter as tk
from tkinter import ttk

"""
the following is a custom theme made for tkinter
11/26/2022
                    ~ wissens

the icon set was created by ___ and can be foun in here https://iconarchive.com/show/beautiful-flat-one-color-icons-by-elegantthemes.2.html
"""

#COLOR PALET DEFINITION
DARKBLUE = "#215d9c"
LIGHGRAY = "#33393b"
GRAY = "#252a2c"
DARKGRAY = "#1b1f20"
BLACK = "#000000"
WHITE = "#fff"
RED = "#ff0000"
GREEN = "#00ff00"

class DarkBlue(ttk.Style):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        #base theme
        self.theme_use("xpnative")

        #TButton
        config = {
            "foreground" : DARKBLUE,
        }

        mapConfig = {}

        self.configure('TButton', **config)
        self.map('TButton', **mapConfig)

        #menuBar.TButton
        config = {
            "foreground" : DARKBLUE,
            "background" : DARKGRAY,
            "width": 20,
        }

        mapConfig = {}

        self.configure('menuBar.TButton', **config)
        self.map('menuBar.TButton', **mapConfig)


        # cursor.TButton
        config = {
            "foreground" : DARKBLUE,
            "background" : DARKGRAY,
        }
        mapConfig = {}

        #cursor.TButton
        self.cursorIcon = tk.PhotoImage(file="./assets/cursor.png")
        config["image"] = self.cursorIcon

        self.configure('cursor.TButton', **config)
        self.map('cursor.TButton', **mapConfig)

        #wall.TButton
        self.wallIcon = tk.PhotoImage(file="./assets/wall.png")
        config["image"] = self.wallIcon

        self.configure('wall.TButton', **config)
        self.map('wall.TButton', **mapConfig)

        #eraser.TButton
        self.eraserIcon = tk.PhotoImage(file="./assets/eraser.png")
        config["image"] = self.eraserIcon

        self.configure('eraser.TButton', **config)
        self.map('eraser.TButton', **mapConfig)

        #start.TButton
        self.startIcon = tk.PhotoImage(file="./assets/start.png")
        config["image"] = self.startIcon

        self.configure('start.TButton', **config)
        self.map('start.TButton', **mapConfig)

        #end.TButton
        self.endIcon = tk.PhotoImage(file="./assets/end.png")
        config["image"] = self.endIcon

        self.configure('end.TButton', **config)
        self.map('end.TButton', **mapConfig)

        #save.TButton
        self.saveIcon = tk.PhotoImage(file="./assets/save.png")
        config["image"] = self.saveIcon

        self.configure('save.TButton', **config)
        self.map('save.TButton', **mapConfig)

        #imageGrid.TButton
        config = {
            "background" : WHITE,
        }

        mapConfig = {}

        self.gridImage = tk.PhotoImage(file="./assets/grid_darkBLue.png")
        config["image"] = self.gridImage

        self.configure('imageGrid.TButton', **config)
        self.map('imageGrid.TButton', **mapConfig)



        #TLabel
        #menuBar.TLabel
        config = {
            "foreground" : WHITE,
            "background" : DARKGRAY,
            "font": ("Helvetica", 10, "bold"),
        }

        mapConfig = {}

        self.configure('menuBar.TLabel', **config)
        self.map('menuBar.TLabel', **mapConfig)

        #menuBarSub.TLabel
        config["font"] = ("Helvetica", 10)

        self.configure('menuBarSub.TLabel', **config)
        self.map('menuBarSub.TLabel', **mapConfig)

        #menuBarSub2.TLabel
        config["font"] = ("Helvetica", 8)

        self.configure('menuBarSub2.TLabel', **config)
        self.map('menuBarSub2.TLabel', **mapConfig)

        #TCombobox
        #no esta funcionando
        config = {
            "state" : "readonly",
        }

        mapConfig = {}

        self.configure('TCombobox', **config)
        self.map('TCombobox', **mapConfig)


        
        

if __name__ == "__main__":
    class App(tk.Tk):
        def __init__(self):
            super().__init__()

            self.geometry("500x500")

            self.style = DarkBlue(self)

            tbutton = ttk.Button(self, text="DarkBlue")
            tbutton.pack()

    app = App()
    app.mainloop()
