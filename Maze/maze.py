import tkinter as tk
from tkinter import messagebox
import random
import queue
import time

from Maze.cell import gridCellButton
from settings import *

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

    #bfs
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
                
