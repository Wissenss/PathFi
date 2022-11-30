import tkinter as tk
from tkinter import ttk

#importa paginas
from menupage import MenuPage
from sandboxpage import SandboxPage

class App(tk.Tk):
    def __init__(self):
        super().__init__()

        # data model
        self.model = {}

        self.model["maze"] = None

        # crea frames
        container = tk.Frame(self)
        container.pack(side="top", fill="both", expand=True)
        container.grid_rowconfigure(0, weight = 1)
        container.grid_columnconfigure(0, weight = 1)

        self.frames = {}
        for F in (MenuPage, SandboxPage):
            frame = F(container, self)
            self.frames[F] = frame
            frame.grid(row=0, column=0, sticky="nsew")

        #llama al metodo para realizar configuraciones de inicio, solo si existe en el frame de la pagina
            try:
                frame.init()
            except:
                pass

        # muestra frame de inicio
        self.renderMenuPage()
        # self.renderSandboxPage()

        #configura ventana
        self.iconbitmap("assets/maze.ico")
        self.title("")

    def showFrame(self, page):
        frame = self.frames[page]
        frame.tkraise() 
        try:
            frame.configWindow()
        except:
            pass

    def renderSandboxPage(self):
        self.showFrame(SandboxPage) 

    def renderMenuPage(self):
        self.showFrame(MenuPage)

if __name__ == "__main__":
    app = App()
    app.mainloop()