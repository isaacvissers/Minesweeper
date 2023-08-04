import tkinter as tk
import random

class minesweeper():
    def __init__(self):
        self.master = tk.Tk()
        self.master.title("Minesweeper")
        self.master.resizable(False, False)
        self.frames = {}
        self.flag = {}
        self.labels = {}
        self.revealed = {}
        self.minePlacement = {}
        self.cols = 9
        self.rows = 9
        self.mines = 10
        self.create_board()
        self.master.mainloop()
        
    def left_click(self, x):
        # Reveal
        if self.minePlacement[x]:
            # Tried to reveal a mine
            print("You Lose")
            quit()
        self.labels[x].configure(text=self.get_adj_mines(x))
        
    def right_click(self, x):
        # Place flag
        self.place_flag(x)

    def place_flag(self, index):
        if not self.flag[index]:
            self.labels[index].configure(text='F')
            self.flag[index] = True
        else:
            self.labels[index].configure(text='')
            self.flag[index] = False
    
    def create_board(self):
        for i in range(self.rows):
            for j in range(self.cols):
                index = str(j) + str(i)
                
                self.frames[index] = tk.Frame(self.master, width=30, height=30, borderwidth=5, relief="raised")
                self.frames[index].grid_propagate(False)
                self.frames[index].grid(row=i, column=j)
                self.frames[index].bind("<Button-1>", lambda x=index: self.left_click(x))
                self.frames[index].bind("<Button-2>", lambda x=index: self.right_click(x))
                self.frames[index].bind("<Button-3>", lambda x=index: self.right_click(x))
                
                self.labels[index] = tk.Label(self.frames[index], text = "")
                self.labels[index].grid(row=i, column=j, sticky='nswe')
                
                self.flag[index] = False
                self.revealed[index] = False
                self.minePlacement[index] = False
        self.set_bombs()
        for i in range(self.rows):
            for j in range(self.cols):
                index = str(j) + str(i)
                if self.minePlacement[index]:
                    self.labels[index]['text'] ='m'
        
                
    def set_bombs(self):
        for i in range(self.mines):
            invalid = True
            while(invalid):
                index = self.get_random_coordinate()
                if not self.minePlacement[index]:
                    self.minePlacement[index] = True
                    invalid = False
            print(self.minePlacement)
            
    def get_random_coordinate(self):
        # return a random valid coordinate
        x = random.randint(0,self.cols-1)
        y  = random.randint(0, self.rows-1)
        index = str(x) + str(y)
        return(index)
        
    def get_adj_mines(self, index):
        # returns the number of mines adjacent (including diagonal) to the clicked square
        # assumes this square is not a mine
        adjMines = 0
        x = int(index[0]) - 1
        y = int(index[1]) - 1
        for i in range(3):
            for j in range (3):
                adjIndex = str(x+i) + str(y+j)
                try:
                    if self.minePlacement[adjIndex]:
                        adjMines += 1
                except KeyError:
                    pass
        return(adjMines)
    
    
    
minesweeper()