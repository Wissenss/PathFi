import tkinter as tk
from tkinter import ttk, messagebox
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
UNVISIT_CELL_COL = "#215d9b"
WALL_COL = DARKBLUE

UP = "U"
RIGHT = "R"
DOWN = "D"  
LEFT = "L"

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

class Maze(tk.Frame):
    def __init__(self, parent, width, height, controller):
        super().__init__(parent)
        self.controller = controller
        self.parent = parent
        self.gridWidth = width
        self.gridHeight = height
        self.gridMaze = []
        self.startCords = None
        self.endCords = None
        self.createGrid()

    # grid methods
    def createGrid(self):
        for i in range(self.gridWidth):
            self.gridMaze.append([])
            for j in range(self.gridHeight):
                cell = gridCellButton(self, self.parent, i, j)
                cell.grid(column=i, row=j, ipadx=0, ipady=0)
                self.gridMaze[i].append(cell)

    def destroyGrid(self):
        for column in self.gridMaze:
            for cell in column:
                cell.destroy()

        self.gridMaze = []

    def clearGrid(self):
        for row in self.gridMaze:
            for cell in row:
                cell.onClickCell("eraser")

    def clearPath(self):
        for row in self.gridMaze:
            for cell in row:
                if (cell.cget("background")==VISIT_CELL_COL or cell.cget("background")==PATH_COL):
                    cell.onClickCell("eraser")

    #maze generation methods
    def mattGrid(self):
        cellsMattGrid = []
        for i, column in enumerate(self.gridMaze):
            if i%2==0 or i==0:
                cellsMattGrid.append([])
            for j, cell in enumerate(column):
                if  (j%2==0 or j==0) and (i%2==0 or i==0):
                    cell.changeState("unvisited_cell")
                    cellsMattGrid[i//2].append((cell, i, j))
                else:
                    cell.onClickCell("wall")
        self.update()       
        return cellsMattGrid

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

            neightbourCell = cells[neightbours_i][neightbours_j][0]
            if neightbourCell.cget("background") == VISITED_CELL_COL or neightbourCell.cget("background") == WHITE:
                self.update()
                continue

            neightbours.append((neightbours_i, neightbours_j))

        return neightbours

    def paintBetweenWall(self, i, j, new_i, new_j, cells, color):
        real_i = cells[i][j][1]
        real_j = cells[i][j][2]

        real_ni = cells[new_i][new_j][1]
        real_nj = cells[new_i][new_j][2]

        wall_i = real_i
        wall_j = real_j

        if real_i<real_ni:
            wall_i += 1
        if real_i>real_ni:
            wall_i-=1
        if real_j<real_nj:
            wall_j += 1
        if  real_j>real_nj:
            wall_j -= 1

        self.gridMaze[wall_i][wall_j].configure(background=color)
        time.sleep(0.05)
        self.update()

    def recursiveBacktracking(self, i, j, cells):
        currentCell = cells[i][j][0]
        currentCell.configure(background = VISITED_CELL_COL)
        self.update()

        for k in range(4):
            neightbours = self.getUnvisitedNeightbours(i, j, cells)

            if not(neightbours):
                currentCell.configure(background=WHITE)
                self.update()
                return

            neightbour = neightbours[random.randint(0, len(neightbours)-1)]
            new_i = neightbour[0]
            new_j = neightbour[1]
            self.paintBetweenWall(i, j, new_i, new_j, cells, VISITED_CELL_COL)
            self.recursiveBacktracking(new_i, new_j, cells)
            self.paintBetweenWall(i, j, new_i, new_j, cells, WHITE)

    def recursiveBacktrackingGeneration(self):
        cells = self.mattGrid()
        self.recursiveBacktracking(0, 0, cells)

    def randomGeneration(self):
        # self.clearGrid()
        density = self.parent.scale.get()
        for row in self.gridMaze:
            for cell in row:
                event = random.randint(0,99)
                if event < density:
                    cell.onClickCell("wall")
                else:
                    cell.onClickCell("eraser")

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
            if(cords[0]<0 or cords[0]>=self.gridWidth or cords[1]<0 or cords[1]>=self.gridHeight):
                return False

            #path crosses wall
            if (self.gridMaze[cords[0]][cords[1]].cget("background") == WALL_COL):
                return False

        #path has cicles
        cell_state = self.gridMaze[cords[0]][cords[1]].cget("background")
        if  cell_state == VISIT_CELL_COL or cell_state == START_COL:
            return False

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

            # self.after(500, lambda: self.gridMaze[cords[0]][cords[1]].changeState("path"))
            self.gridMaze[cords[0]][cords[1]].configure(background=PATH_COL)
            time.sleep(0.1)
            self.update()

        time.sleep(0.1)
        self.gridMaze[self.endCords[0]][self.endCords[1]].configure(background=PATH_COL)
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

        cell = self.gridMaze[cords[0]][cords[1]]
        if cell.cget("background") == VISIT_CELL_COL:
            cell.changeState("visited_cell")
        elif cell.cget("background") == WHITE:
            cell.changeState("visit_cell")
        else:
            pass

        time.sleep(0.005)
        self.update()

    def bfs(self):
        self.clearPath()
        paths = queue.Queue()
        path = []
        paths.put(path)
        while(True):
            if paths.empty():
                messagebox.showinfo("", "This maze has no solution")
                return

            path = paths.get()

            for direction in [UP, DOWN, RIGHT, LEFT]:
                new_path = [step for step in path]
                new_path.append(direction)
                if self.isValidPath(new_path):
                    paths.put(new_path)
                    self.renderPosiblePath(new_path)
                    if(self.isSolutionPath(new_path)):
                        self.renderPath(new_path)
                        return
                

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
        self.heightScale.set(self.parent.maze.gridWidth)
        self.heightScale.grid(column=0, row=1)

        self.widthScale = tk.Scale(settings, from_=5, to=40, orient=tk.HORIZONTAL, troughcolor=DARKBLUE, highlightthickness=0)
        self.widthScale.set(self.parent.maze.gridHeight)
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
        self.parent.maze.gridWidth = self.widthScale.get()
        self.parent.maze.gridHeight = self.heightScale.get()
        self.parent.maze.destroyGrid()
        self.parent.maze.createGrid()
        self.destroy()

class SandboxPage(tk.Frame):
    def __init__(self, container, controller:tk.Tk):
        super().__init__(container)
        self.controller = controller

        #CONTROL VARIABLES
        self.selectedTool = None

        self.defaultGridWidth = 10
        self.defaultGridHeight = 10

        #**MENUBAR**
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

        generation_algos = ["Select An Algorithm", "Random", "Recursive Backtracking"] # 

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


        #**MAZE GRID**
        self.maze = Maze(self, self.defaultGridWidth, self.defaultGridHeight, self.controller)
        self.maze.pack(expand=1) 

    #**configuration mehtods**
    #render with proper dimensions
    def configWindow(self):
        self.controller.geometry("900x700")
        self.controller.resizable(False, False)
        # maybe add logic to render in the center of the screen?

    #initialize with default values
    def init(self):
        self.cbmazefin.current(0)
        self.cbmazegen.current(0)
        self.bfind.configure(state=tk.DISABLED)
        self.bgenerate.configure(state=tk.DISABLED)
        self.selectedTool = "cursor"

    #**menubar methods**
    #tool selection
    def selectTool(self, tool):
        self.selectedTool = tool

    #settings menu
    def settingsMenu(self):
        SettingsMenu(self, self.controller)

    #maze generation controlls 
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

    def generateMaze(self):
        selection = self.cbmazegen.get()
        self.maze.startCords = None
        self.maze.endCords = None

        if selection == "Random":
            self.maze.randomGeneration()
        elif selection == "Recursive Backtracking":
            self.maze.recursiveBacktrackingGeneration()
        else:
            pass

    #path finding controlls
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

    def findPath(self):
        #check that maze is valid
        isValidMaze = True
        errors = ""
        if self.maze.startCords == None:
            isValidMaze = False
            errors += "A maze should have a Starting Point\n"
        if self.maze.endCords == None:
            isValidMaze = False
            errors += "A maze should have an End Point\n"
        if not(isValidMaze):
            messagebox.showwarning("Not valid", errors)
            return

        #if maze is valid, call maze solvers
        selection = self.cbmazefin.get()
        if selection == "Breath First Search":
            self.maze.bfs()
