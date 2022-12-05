import tkinter as tk
from tkinter import ttk, messagebox

from settings import *
from Maze.maze import Maze

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
        self.controller.resizable(True, True)
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
