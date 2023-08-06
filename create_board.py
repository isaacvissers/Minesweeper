import tkinter as tk
import random


class minesweeper():
    def __init__(self):
        # Initialize the tkinter GUI
        self.master = tk.Tk()
        self.master.title("Minesweeper")
        self.master.resizable(False, False)
        
        # dictionaries used to store data at each square
        self.frames = {}
        self.flag = {}
        self.labels = {}
        self.revealed = {}
        self.minePlacement = {}
        self.invalidPlacement = {}
        
        # Initialize the size and general properties
        self.firstClick = True
        self.cols = 9
        self.rows = 9
        self.mines = 10
        self.remainingMines = 10
        
        self.create_board()
        self.master.mainloop()
        
    def reveal_square(self, event, index):
        # Reveal the square "index"
        if self.flag[index]:
            # Must remove flag before you can reveal a square
            self.complete_check()
            return
        
        if self.firstClick:
            # if this is the first click we must place the mines, and no mines can be adjacent to the click
            self.firstClick = False
            self.first_click(index)
            
        if self.minePlacement[index] & (event == 0):
            # Revealed a mine
            print("You Lose")
            quit()

        if self.revealed[index]:
            # Reveals adjacent for correct number of adjacent flags - THIS CODE DOESNT CURRENTLY WORK
            if self.get_adj_flags(index) == self.get_adj_mines(index):
                self.reveal_adjacent(index)
            self.complete_check()
            return
        # Reveal square
        self.revealed[index] = True
        adjMines = self.get_adj_mines(index)
        self.labels[index].configure(text=adjMines)
        
        if adjMines == 0:
            x = int(index[0]) - 1
            y = int(index[1]) - 1
            for i in range(3):
                for j in range (3):
                    adjIndex = str(x+i) + str(y+j)
                    if (0 <= x+i < self.cols) and (0 <= y+j < self.rows):
                        self.reveal_adjacent(adjIndex)
        else:
            self.complete_check()
            return
        
        
    def right_click(self, event, x):
        # Place flag
        if not self.revealed[x]:
            # Makes sure flag isnt on already revealed square
            self.place_flag(x)
            self.remainingMines -= 1
            self.complete_check()

    def place_flag(self, index):
        # Toggles flag for undiscovered square
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
                self.frames[index].bind("<Button-1>", lambda event, x=index: self.reveal_square(event, x))
                self.frames[index].bind("<Button-2>", lambda event, x=index: self.right_click(event, x))
                self.frames[index].bind("<Button-3>", lambda event, x=index: self.right_click(event, x))
                
                self.labels[index] = tk.Label(self.frames[index], text = "")
                self.labels[index].grid(row=i, column=j, sticky='nswe')
                
                self.labels[index].bind("<Button-1>", lambda event, x=index: self.reveal_square(event, x))
                self.labels[index].bind("<Button-2>", lambda event, x=index: self.right_click(event, x))
                self.labels[index].bind("<Button-3>", lambda event, x=index: self.right_click(event, x))                
                
                self.flag[index] = False
                self.revealed[index] = False
                self.minePlacement[index] = False
                self.invalidPlacement[index] = False

                
    def set_bombs(self):
        # Sets the position of all of the bombs
        for i in range(self.mines):
            invalid = True
            while(invalid):
                index = self.get_random_coordinate()
                if not self.invalidPlacement[index]:
                    self.minePlacement[index] = True
                    self.invalidPlacement[index] = True
                    invalid = False
            
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
    
    def get_adj_flags(self, index):
        # returns the number of mines adjacent (including diagonal) to the clicked square
        # assumes this square is not a mine
        adjMines = 0
        x = int(index[0]) - 1
        y = int(index[1]) - 1
        for i in range(3):
            for j in range (3):
                adjIndex = str(x+i) + str(y+j)
                try:
                    if self.flag[adjIndex]:
                        adjMines += 1
                except KeyError:
                    pass
        return(adjMines)
    
    def reveal_adjacent(self, index):
        # Reveal
        if self.flag[index] or self.minePlacement[index]:
            # Must remove flag before you can remove a square
            return
        if self.revealed[index]:
            print('TESTING')
            return
        self.revealed[index] = True
        adjMines = self.get_adj_mines(index)
        self.labels[index].configure(text=adjMines)
        if adjMines == 0:
            x = int(index[0]) - 1
            y = int(index[1]) - 1
            for i in range(3):
                for j in range (3):
                    adjIndex = str(x+i) + str(y+j)
                    if (0 <= x+i < self.cols) and (0 <= y+j < self.rows):
                        # Reveals adjacent squares within boundaries of the board
                        self.reveal_adjacent(adjIndex)
        else:
            # if there is an adjacent mine, no need to keep revealing
            return
    
    def complete_check(self):
        for i in range(self.rows):
            for j in range(self.cols):
                index = str(j) + str(i)
                if not self.revealed[index]:
                    if not self.minePlacement[index]:
                        return 
        print("You Won!")
        quit()
        
    def first_click(self, index):
        x = int(index[0]) - 1
        y = int(index[1]) - 1
        for i in range(3):
            for j in range (3):
                adjIndex = str(x+i) + str(y+j)
                self.invalidPlacement[adjIndex] = True
        self.set_bombs()
        for i in range(self.rows):
            for j in range(self.cols):
                index = str(j) + str(i)
                if self.minePlacement[index]:
                    # For testing only
                    self.labels[index]['text'] ='m' 
        return
    
# initaite the class that runs the games
minesweeper()