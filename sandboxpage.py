import tkinter as tk
from tkinter import ttk
import random
import queue
import time

DARKBLUE = "#215d9c"
DARKGRAY = "#1b1f20"
WHITE = "#fff"
RED = "#ff0000"
GREEN = "#00ff00"
ORANGE = "#fc5603"
GREEN = "#b3d91e"
GOLDEN = "#ffbf00"
DIMBLUE = "#9bb4c5" #"#216b9c"
LIGHTBLUE = "#9bb4c4" #"#6088a1" #"#427a9e"
LIGHGRAY = "#33393b"
LIGHTRED = "#c4a59b"
DARKRED = "#e33917"

START_COL = ORANGE
END_COL = GREEN
PATH_COL = GOLDEN
VISITED_CELL_COL = LIGHTBLUE
VISIT_CELL_COL = DIMBLUE
UNVISIT_CELL_COL = LIGHTRED
WALL_COL = DARKBLUE

UP = "U"
RIGHT = "R"
DOWN = "D"
LEFT = "L"

#icon set: https://iconarchive.com/show/beautiful-flat-one-color-icons-by-elegantthemes.2.html

class gridCellButton(tk.Button):
    def __init__(self, parent, controller, i, j):
        # self.start_icon = tk.PhotoImage("./assets/start_small.png")
        cell_width = 2
        cell_height = 7
        self.i = i
        self.j = j
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
            if ((self.i, self.j) == self.controller.startCords):
                self.controller.startCords = None

            if ((self.i, self.j) == self.controller.endCords):
                self.controller.endCords = None
            # self.configure(image=None)
        elif tool == "start":
            self.configure(background=START_COL)

            previous_cords = self.controller.startCords
            if previous_cords != None:
                self.controller.mazeGrid[previous_cords[0]][previous_cords[1]].onClickCell("eraser")
            self.controller.startCords = (self.i, self.j)
            # self.configure(image=self.start_icon)
        elif tool == "end":
            self.configure(background=END_COL)

            previous_cords = self.controller.endCords
            if previous_cords != None:
                self.controller.mazeGrid[previous_cords[0]][previous_cords[1]].onClickCell("eraser")
            self.controller.endCords = (self.i, self.j)
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

class SettingsMenu(tk.Toplevel):
    def __init__(self, parent, controller:tk.Tk):
        super().__init__()
        self.parent = parent

        self.geometry("400x300")
        self.grab_set()
        self.transient(None)
        self.title("Settings")
        self.resizable(0, 0)
        self.iconbitmap("./assets/settings.ico")

        #configurations settings
        settings = tk.Frame(self)
        settings.pack(expand=1)
        
        self.heightScale = tk.Scale(settings, from_=5, to=40, troughcolor=DARKBLUE, highlightthickness=0)
        self.heightScale.set(parent.grid_width)
        self.heightScale.grid(column=0, row=1)

        self.widthScale = tk.Scale(settings, from_=5, to=40, orient=tk.HORIZONTAL, troughcolor=DARKBLUE, highlightthickness=0)
        self.widthScale.set(parent.grid_width)
        self.widthScale.grid(column=1, row=0)

        # self.gridImage = tk.PhotoImage("./assets/grid.png")
        # gridPicture = tk.Label(settings, image=self.gridImage)
        # gridPicture.grid(column=1, row=1)

        gridImage = ttk.Label(settings, style="imageGrid.TButton")
        gridImage.grid(column=1, row=1)

        #navegarion controls
        bottomControls = tk.Frame(self, background=DARKGRAY)
        bottomControls.pack(side="bottom", fill="both")

        bcancel = ttk.Button(bottomControls, text="Cancel", style="menuBar.TButton", width=10, command=self.destroy)
        bcancel.pack(side="right", padx=(5,5), pady=(5,5))

        baccept = ttk.Button(bottomControls, text="Accept", style="menuBar.TButton", width=10, command=self.accept)
        baccept.pack(side="right", padx=(0,5), pady=(5,5))

    # def move(self, e):
    #     self.geometry(f"+{e.x_root}+{e.y_root}")

    def accept(self):
        self.parent.grid_width = self.widthScale.get()
        self.parent.grid_height = self.heightScale.get()
        self.parent.destroyGrid()
        self.parent.createGrid()
        self.destroy()

class SandboxPage(tk.Frame):
    def __init__(self, container, controller:tk.Tk):
        super().__init__(container)
        self.controller = controller

        #CONTROL VARIABLES
        self.selectedTool = None
        self.startCords = None
        self.endCords = None

        self.mazeGrid = []
        self.grid_width = 10
        self.grid_height = 10

        #MENUBAR
        menubar = tk.Frame(self, background=DARKGRAY, padx=10, pady=10)
        menubar.pack(side="left", fill="both")

        #top section
        topSection = tk.Frame(menubar, background=DARKGRAY)
        topSection.pack(side="top")

        # back to main menu
        bback = ttk.Button(topSection, text="Menu", style="menuBar.TButton", command=controller.renderMenuPage)
        bback.grid(column=0, row=0)

        # search algorithm
        pathFindingmenu = tk.Frame(topSection, background=DARKGRAY)
        pathFindingmenu.grid(column=0, row=1, pady=(20, 0),  sticky="NSWE")

        label = ttk.Label(pathFindingmenu, text="Path Finding", style="menuBar.TLabel")
        label.grid(column=0, row=0, sticky="W", pady=(0,5))

        finding_algos = ["Select An Algorithm", "Breath First Search"]

        cbmazefin = ttk.Combobox(pathFindingmenu, values=finding_algos, state="readonly")
        cbmazefin.grid(column=0, row=1, pady=(0,10))
        cbmazefin.bind("<<ComboboxSelected>>", self.onSelectionChangedPathfin)
        self.cbmazefin = cbmazefin
        

        find = ttk.Button(pathFindingmenu, text="Find", style="menuBar.TButton", command=self.findPath)
        find.grid(column=0, row=2, pady=(0,10))
        self.bfind = find

        # maze generation
        mazeGenerationmenu = tk.Frame(topSection, background=DARKGRAY)
        mazeGenerationmenu.grid(column=0, row=2, pady=(40,0), sticky="NSWE")
        self.mazeGenerationmenu = mazeGenerationmenu

        label = ttk.Label(mazeGenerationmenu, text="Maze Generation", style="menuBar.TLabel")
        label.grid(column=0, row=0, sticky="W", pady=(0,5))

        generation_algos = ["Select An Algorithm", "Random",] # "Recursive Backtracking"

        cbmazegen = ttk.Combobox(mazeGenerationmenu, values=generation_algos, state="readonly")
        cbmazegen.grid(column=0, row=1, pady=(0,10))
        cbmazegen.bind("<<ComboboxSelected>>", self.onSelectionChangedMazeGen)
        self.cbmazegen = cbmazegen
        
        # optional controls to tweak maze generation | render at runtime | handle by onSelectionChangeMazeGen
        self.mazeGenAditionalControl = tk.Frame(mazeGenerationmenu, background=DARKGRAY)
        self.mazeGenAditionalControl.grid(column=0, row=2, pady=(0,0))

        self.scaleLabel = None
        self.scale = None

        generate = ttk.Button(mazeGenerationmenu, text="Generate", style="menuBar.TButton", command=self.generateMaze)
        generate.grid(column=0, row=2, pady=(0,10))
        self.bgenerate=generate


        #bottom section 
        bottomSection = tk.Frame(menubar, background=DARKGRAY)
        bottomSection.pack(side="bottom", fill="both")
        # edit tools
        editTools = tk.Frame(bottomSection, background=DARKGRAY)
        editTools.grid(column=0, row=0, pady=(20, 20), sticky="WES")

        label = ttk.Label(editTools, text="Tools", style="menuBar.TLabel")
        label.pack(side="top", anchor="nw")

        tools = tk.Frame(editTools, background=DARKGRAY)
        tools.pack(expand=1,)

        cursorTool = ttk.Button(tools, style="cursor.TButton", command=lambda:self.selectTool("cursor"))
        cursorTool.grid(column=0, row=0, pady=(5,5), padx=(5,5))

        saveTool = ttk.Button(tools, style="save.TButton", state=tk.DISABLED, command=lambda:self.selectTool("save"))
        saveTool.grid(column=1, row=0, pady=(5,5), padx=(5,5))

        wallTool = ttk.Button(tools, style="wall.TButton", command=lambda:self.selectTool("wall"))
        wallTool.grid(column=0, row=1, pady=(5,5), padx=(5,5))

        eraserTool = ttk.Button(tools, style="eraser.TButton", command=lambda:self.selectTool("eraser"))
        eraserTool.grid(column=1, row=1, pady=(5,5), padx=(5,5))

        startTool = ttk.Button(tools, style="start.TButton", command=lambda:self.selectTool("start"))
        startTool.grid(column=0, row=2, pady=(5,5), padx=(5,5))

        endTool = ttk.Button(tools, style="end.TButton", command=lambda:self.selectTool("end"))
        endTool.grid(column=1, row=2, pady=(5,5), padx=(5,5))

        # configuration menu
        configMenu = ttk.Button(bottomSection, text="Settings", style="menuBar.TButton", command=self.settingsMenu)
        configMenu.grid(column=0, row=1, padx=(5,5))


        #MAZE GRID
        self.mazegrid = tk.Canvas(self)
        self.mazegrid.pack(expand=1) 
        self.createGrid()


    # configuration mehtods
    def configWindow(self):
        self.controller.geometry("900x700")
        self.controller.resizable(False, False)
        # self.controller.eval('tk::PlaceWindow . center')

    def init(self):
        self.cbmazefin.current(0)
        self.cbmazegen.current(0)
        self.bfind.configure(state=tk.DISABLED)
        self.bgenerate.configure(state=tk.DISABLED)
        self.selectedTool = "cursor"

    # grid methods
    def createGrid(self):
        for i in range(self.grid_width):
            self.mazeGrid.append([])
            for j in range(self.grid_height):
                cell = gridCellButton(self.mazegrid, self, i, j)
                cell.grid(column=i, row=j, ipadx=0, ipady=0)
                self.mazeGrid[i].append(cell)

    def destroyGrid(self):
        for column in self.mazeGrid:
            for cell in column:
                cell.destroy()

        self.mazeGrid = []

    def clearGrid(self):
        for row in self.mazeGrid:
            for cell in row:
                cell.onClickCell("eraser")

    def mattGrid(self):
        cellsGrid = []
        for i, column in enumerate(self.mazeGrid):
            cellsGrid.append([])
            for j, cell in enumerate(column):
                if i%2==0 and j%2==0:
                    cell.changeState("unvisited_cell")
                    cellsGrid[i].append({"grdiCords" : (i, j), "visited":False})
                else:
                    cell.onClickCell("wall")
                    
        return cellsGrid

    def getUnvisitedNeightbours(self, current_i, current_j, cells):
        neightbours = []

        for direction in [UP, RIGHT, DOWN, LEFT]:
            neightbours_i = current_i
            neightbours_j = current_j
            if direction == UP:
                neightbours_j -= 1
            if direction == DOWN:
                neightbours_j += 1
            if direction == RIGHT:
                neightbours_i += 1
            if direction == LEFT:
                neightbours_i -= 1

            if neightbours_i < 0 or neightbours_i >= len(cells[0]) or neightbours_j < 0 or neightbours_j >= len(cells):
                continue

            if cells[neightbours_i][neightbours_j]["visited"]:
                continue

            neightbours.append(cells[neightbours_i][neightbours_j])

        return neightbours

    #maze generation methods
    def randomGeneration(self):
        # self.clearGrid()
        density = self.scale.get()
        for row in self.mazeGrid:
            for cell in row:
                event = random.randint(0,99)
                if event < density:
                    cell.onClickCell("wall")
                else:
                    cell.onClickCell("eraser")

    def recursiveBacktrackingGeneration(self, i=0, j=0):
        cells = self.mattGrid()
        cells[i][j]["visited"] = True
        neightbours = self.getUnvisitedNeightbours(i, j, cells)
        
    def generateMaze(self):
        selection = self.cbmazegen.get()
        self.startCords = None
        self.endCords = None

        if selection == "Random":
            self.randomGeneration()
        elif selection == "Recursive Backtracking":
            self.recursiveBacktrackingGeneration()
        else:
            pass

    #path finding methods
    def isSolutionPath(self, path):
        cords = [self.startCords[0], self.startCords[1]]        

        for step in path:
            if step==UP:
                cords[1] -= 1
            if step==DOWN:
                cords[1] += 1
            if step==RIGHT:
                cords[0] += 1
            if step==LEFT:
                cords[0] -= 1

            if (cords[0], cords[1]) == self.endCords:
                return True
        
        return False

    def isValidPath(self, path):
        cords = [self.startCords[0], self.startCords[1]] 
        visitedCells = []
        # previousCords = [self.startCords[0], self.startCords[1]] 

        # try:
        for step in path:
            if step==UP:
                cords[1] -= 1
            if step==DOWN:
                cords[1] += 1
            if step==RIGHT:
                cords[0] += 1
            if step==LEFT:
                cords[0] -= 1

            #path goes out of grid
            if(cords[0]<0 or cords[0]>=self.grid_width or cords[1]<0 or cords[1]>=self.grid_height):
                return False

            #path crosses wall
            if (self.mazeGrid[cords[0]][cords[1]].cget("background") == WALL_COL):
                return False

            #path goes backwards
            # if (cords==previousCords):
            #     return False

            for cell in visitedCells:
                if cell == self.mazeGrid[cords[0]][cords[1]]:
                    return False

                if cell.cget("background") == START_COL:
                    return False

            visitedCells.append(self.mazeGrid[cords[0]][cords[1]])

            # previousCords = [cords[0], cords[1]]

        # except: #path goes out of bounds
        #     return False     

        return True  

    def renderPath(self, path):
        cords = [self.startCords[0], self.startCords[1]]

        for step in path:
            if step==UP:
                cords[1] -= 1
            if step==DOWN:
                cords[1] += 1
            if step==RIGHT:
                cords[0] += 1
            if step==LEFT:
                cords[0] -= 1

            # self.after(500, lambda: self.mazeGrid[cords[0]][cords[1]].changeState("path"))
            self.mazeGrid[cords[0]][cords[1]].configure(background=PATH_COL)
            time.sleep(0.1)
            self.update_idletasks()


        self.endCords = None

    def renderPosiblePath(self, path):
        cords = [self.startCords[0], self.startCords[1]]

        for step in path:
            if step==UP:
                cords[1] -= 1
            if step==DOWN:
                cords[1] += 1
            if step==RIGHT:
                cords[0] += 1
            if step==LEFT:
                cords[0] -= 1

        cell = self.mazeGrid[cords[0]][cords[1]]
        if cell.cget("background") == VISIT_CELL_COL:
            cell.changeState("visited_cell")
        elif cell.cget("background") == WHITE:
            cell.changeState("visit_cell")
        else:
            pass

        time.sleep(0.01)
        self.update()

    def bfs(self):
        paths = queue.Queue()
        path = []
        paths.put(path)
        while(True):
            path = paths.get()

            if(self.isSolutionPath(path)):
                return path

            for direction in [UP, RIGHT, DOWN, LEFT]:
                new_path = [step for step in path]
                new_path.append(direction)
                if self.isValidPath(new_path):
                    paths.put(new_path)
                    self.renderPosiblePath(new_path)
            # time.sleep(0.01)
            
    def findPath(self):
        selection = self.cbmazefin.get()

        if selection == "Breath First Search":
            path = self.bfs()
            self.renderPath(path)

    #menubar methods
    def selectTool(self, tool):
        self.selectedTool = tool

    def onSelectionChangedMazeGen(self, event):
        selection = self.cbmazegen.get()

        if selection == "Select An Algorithm":
            self.bgenerate.configure(state=tk.DISABLED)
        elif selection != None:
            self.bgenerate.configure(state=tk.ACTIVE)
        else:
            self.bgenerate.configure(state=tk.DISABLED)
            print("Error Unhandle selection event for maze generation combobox")
            return

        try:
            self.configlabel.destroy()
            self.scaleLabel.destroy()
            self.scale.destroy()
            self.additionalControls.destroy()
            # self.update()
        except:
            pass

        #render aditional controls
        if selection == "Random":
            self.mazeGenAditionalControl = tk.Frame(self.mazeGenerationmenu, background=DARKGRAY)
            self.mazeGenAditionalControl.grid(column=0, row=3, pady=(0,0), padx=(0,0))

            self.configlabel = ttk.Label(self.mazeGenAditionalControl, text="Parameters", style="menuBarSub.TLabel", width=20)
            self.configlabel.pack(side="top", anchor="nw")

            self.additionalControls = tk.Frame(self.mazeGenAditionalControl, background=DARKGRAY)
            self.additionalControls.pack(fill="both", anchor="center", expand=1)

            self.scaleLabel = ttk.Label(self.additionalControls, text="Density:", style="menuBarSub2.TLabel")
            self.scaleLabel.grid(column=0, row=0, sticky="s")

            self.scale = tk.Scale(self.additionalControls, from_=0, to=100, orient=tk.HORIZONTAL, background=DARKGRAY, troughcolor=DARKBLUE, foreground=WHITE, highlightthickness=0)
            self.scale.set(42)
            self.scale.grid(column=1, row=0, sticky="NSWE")

    def onSelectionChangedPathfin(self, event):
        selection = self.cbmazefin.get()

        if selection == "Select An Algorithm":
            self.bfind.configure(state=tk.DISABLED)
        elif selection != None:
            self.bfind.configure(state=tk.ACTIVE)
        else:
            self.bfind.configure(state=tk.DISABLED)
            print("Error Unhandle selection event for path finding combobox")
            return

    def settingsMenu(self):
        SettingsMenu(self, self.controller)