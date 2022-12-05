import tkinter as tk
from settings import *

class gridCellButton(tk.Button):
    def __init__(self, parent, controller, i, j):
        # self.start_icon = tk.PhotoImage("./assets/start_small.png")
        cell_width = 2
        cell_height = 7
        self.i = i
        self.j = j
        self.parent = parent
        self.controller = controller

        settings = {
                "width":cell_width,
                "font":("Helvetica", cell_height),
                "background":WHITE,
                "borderwidth":1,
                "padx":0, 
                "pady":0,
                "relief":"solid",
                "command": lambda: self.onClickCell(self.controller.selectedTool),
            }

        super().__init__(parent, **settings)

    def onClickCell(self, tool):
        if  tool == "cursor":
            pass
        elif tool == "wall":
            self.configure(background=DARKBLUE)
            # self.configure(image=None)
        elif tool == "eraser":
            self.configure(background=WHITE)
            if ((self.i, self.j) == self.parent.startCords):
                self.parent.startCords = None

            if ((self.i, self.j) == self.parent.endCords):
                self.parent.endCords = None
            # self.configure(image=None)
        elif tool == "start":
            self.configure(background=START_COL)

            previous_cords = self.parent.startCords
            if previous_cords != None:
                self.parent.gridMaze[previous_cords[0]][previous_cords[1]].onClickCell("eraser")
            self.parent.startCords = (self.i, self.j)
            # self.configure(image=self.start_icon)
        elif tool == "end":
            self.configure(background=END_COL)

            previous_cords = self.parent.endCords
            if previous_cords != None:
                self.parent.gridMaze[previous_cords[0]][previous_cords[1]].onClickCell("eraser")
            self.parent.endCords = (self.i, self.j)
        else:
            print("Hey there, something went wrong!!!!")

    def changeState(self, state):
        if state == "wall":
            self.configure(background=WALL_COL)
        
        if state == "visit_cell":
            self.configure(background=VISIT_CELL_COL)

        if state == "visited_cell":
            self.configure(background=VISITED_CELL_COL)

        if state == "path":
            self.configure(background=PATH_COL)

        if state == "unvisited_cell":
            self.configure(background=UNVISIT_CELL_COL)

