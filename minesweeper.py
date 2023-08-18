# Import necessary packages
import tkinter as tk
import random
import time
from PIL import Image, ImageTk
from tkinter import ttk


class Minesweeper():
# The class for the game board
    def __init__(self):
        # Initialize the tkinter GUI
        self.master = tk.Tk()
        self.master.title("Minesweeper")
        self.master.resizable(False, False)
        self.boardFrame = tk.Frame(self.master)
        self.boardFrame.grid(row=1, column=0)
        
        # Create necessary images
        self.flagImage = Image.open('flag.png')
        self.mineImage = Image.open('mine.png')
        self.flagImage = self.flagImage.resize((23, 23))
        self.mineImage = self.mineImage.resize((23, 23))
        self.flagImage = ImageTk.PhotoImage(self.flagImage)
        self.mineImage = ImageTk.PhotoImage(self.mineImage)
        
        # Initialize the GUI
        self.create_menu()
        self.master.mainloop()
        
    def reveal_square(self, event, index):
        # Reveal the square at index
        if self.flag[index]:
            # Must remove flag before you can reveal a square
            return
        
        if self.firstClick:
            # No mines can be adjacent
            self.firstClick = False
            self.first_click(index)
            
        if self.minePlacement[index]:
            # Clicked a mine
            self.stopwatch.stop()
            print("You Lose")
            self.display_mines()
            self.labels[index].configure(bg='red')
            self.frames[index].configure(bg='red')
            self.master.update()
            time.sleep(5)
            self.reset()
            return

        # Reveal square
        self.revealed[index] = True
        self.labels[index].configure(background="#A9A9A9")
        self.frames[index].configure(bg='#A9A9A9', borderwidth=1)
        adjMines = self.get_adj_mines(index)
        if adjMines != 0:
            self.labels[index].configure(text=adjMines)
        self.master.update()
        if adjMines == 0:
            x = int(index[0]) - 1
            y = int(index[1]) - 1
            for i in range(3):
                for j in range (3):
                    adjIndex = (x+i, y+j)
                    if (0 <= x+i < self.cols) and (0 <= y+j < self.rows):
                        self.reveal_adjacent(adjIndex)
        else:
            self.complete_check()
            return
        
    def right_click(self, event, index):
        # Place flag
        if not self.revealed[index]:
            # Makes sure flag isnt on already revealed square
            self.place_flag(index)
            self.remainingMines -= 1
            self.complete_check()

    def place_flag(self, index):
        # Toggles flag for undiscovered square
        if not self.flag[index]:
            self.frames[index].configure(borderwidth=1)
            self.labels[index].configure(image=self.flagImage)
            self.frames[index].configure(bg='#A9A9A9')
            self.labels[index].configure(bg='#A9A9A9')
            self.flag[index] = True
        else:
            self.labels[index].configure(image='')
            self.frames[index].configure(borderwidth=5)
            self.frames[index].configure(bg='#36454F')
            self.labels[index].configure(bg='#36454F')
            self.flag[index] = False
    
    def create_board(self):
        # Reconfigure board area
        self.resetButton.configure(text='Reset')
        self.reset()
        self.get_size() 
        
        # Create board 
        for i in range(self.rows):
            for j in range(self.cols):
                index = (j, i)   
                self.frames[index] = tk.Frame(self.boardFrame, width=30, height=30, borderwidth=5, relief="raised", background="#36454F")
                self.frames[index].grid_propagate(False)
                self.frames[index].grid(row=i+1, column=j)
                self.frames[index].bind("<Button-1>", lambda event, x=index: self.reveal_square(event, x))
                self.frames[index].bind("<Button-2>", lambda event, x=index: self.right_click(event, x))
                self.frames[index].bind("<Button-3>", lambda event, x=index: self.right_click(event, x))
                
                self.labels[index] = tk.Label(self.frames[index], text = "", background="#36454F")
                self.labels[index].grid(row=0, column=0)

                self.labels[index].bind("<Button-1>", lambda event, x=index: self.reveal_square(event, x))
                self.labels[index].bind("<Button-2>", lambda event, x=index: self.right_click(event, x))
                self.labels[index].bind("<Button-3>", lambda event, x=index: self.right_click(event, x))                
                
                # Set properties for each square
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
        index = (x, y)
        return(index)
        
    def get_adj_mines(self, index):
        # returns the number of mines adjacent (including diagonal) to the clicked square
        # assumes this square is not a mine
        adjMines = 0
        x = int(index[0]) - 1
        y = int(index[1]) - 1
        for i in range(3):
            for j in range (3):
                adjIndex = (x+i, y+j)
                try:
                    if self.minePlacement[adjIndex]:
                        adjMines += 1
                except KeyError:
                    pass
        return(adjMines)
    
    def reveal_adjacent(self, index):
        if self.flag[index] or self.minePlacement[index]:
            # Shouldnt be revealing
            return
        if self.revealed[index]: 
            # Already Revealed
            return
        # Reveal square
        self.labels[index].configure(background="#A9A9A9")
        self.frames[index].configure(bg='#A9A9A9', borderwidth=1)
        self.revealed[index] = True
        adjMines = self.get_adj_mines(index)
        if adjMines != 0:
            # Stop growing revealed area
            self.labels[index].configure(text=adjMines)
            return
        else:
            # Recursivly call for each adjacent share
            x = int(index[0]) - 1
            y = int(index[1]) - 1
            for i in range(3):
                for j in range (3):
                    adjIndex = (x+i, y+j)
                    if (0 <= x+i < self.cols) and (0 <= y+j < self.rows):
                        # Reveals adjacent squares within boundaries of the board
                        self.reveal_adjacent(adjIndex)

    def complete_check(self):
        # check if every square is either a flag or revelead
        for i in range(self.rows):
            for j in range(self.cols):
                index = (j, i)
                if not self.revealed[index]:
                    if not self.minePlacement[index]:
                        return 
        # Game is complete
        self.stopwatch.stop()
        elapsed = self.stopwatch.elapsed_time
        minutes = int(elapsed // 60)
        seconds = int(elapsed % 60)
        time_str = f"{minutes:02d}:{seconds:02d}"
        print("You Won in " + time_str + " minutes!")

        self.labels[index].configure(background="#A9A9A9")
        self.frames[index].configure(bg='#A9A9A9', borderwidth=1)
        time.sleep(5)
        
    def first_click(self, index):
        # Set bombs so that none are adjacent and reveal this square
        x = int(index[0]) - 1
        y = int(index[1]) - 1
        for i in range(3):
            for j in range (3):
                adjIndex = (x+i, y+j)
                self.invalidPlacement[adjIndex] = True
        self.set_bombs()
        self.stopwatch.start()
        return
    
    def display_mines(self):
        # Display all of the mines
        for i in range(self.rows):
            for j in range(self.cols):
                index = (j, i)
                if self.minePlacement[index]:
                    self.frames[index].configure(borderwidth=1)
                    self.labels[index].configure(image=self.mineImage)
                    self.frames[index].configure(bg='#A9A9A9')
                    self.labels[index].configure(bg='#A9A9A9')
                    self.flag[index] = True
        self.master.update()

    def create_menu(self):
        # Set up frame
        self.menuFrame = tk.Frame(self.master)
        self.menuFrame.grid(row=0, column=0, columnspan=100, padx=10)
        
        # Create stopwatch widget
        self.stopwatchFrame = tk.Frame(self.menuFrame)
        self.stopwatchFrame.grid(row=0, column=0)
        self.stopwatch = StopwatchApp(self.stopwatchFrame)
        
        # Create reset button and difficulty selector
        self.resetButton = tk.Button(self.menuFrame, text='Start', font="Helvetica 12", command=self.create_board)
        self.resetButton.grid(row=0, column=1, columnspan=5, pady=5, padx=10)
        
        self.difficultyFrame = tk.Frame(self.menuFrame)
        self.difficultyFrame.grid(row=0, column=8, columnspan=3)
        self.difficulty = tk.StringVar()
        self.difficulties = ['Easy', 'Medium', 'Hard', 'Very Hard']
        self.difficultyBox = ttk.Combobox(self.difficultyFrame, textvariable=self.difficulty, width=10)
        self.difficultyBox.grid(row=0, column=2, pady=10, sticky='nsew', padx=10)
        self.difficultyBox.config(values = self.difficulties)
        self.difficultyBox.set('Easy')
            
    def get_size(self):
        # Uses the difficulty setting and returns the correct size
        if self.difficulty.get() == 'Easy':
            self.rows = 9
            self.cols = 9
            self.mines = 10
            self.remainingMines = 10
        elif self.difficulty.get() == 'Medium':
            self.rows = 16
            self.cols = 16
            self.mines = 40
            self.remainingMines = 40
        elif self.difficulty.get() == 'Hard':
            self.rows = 16
            self.cols = 30
            self.mines = 99
            self.remainingMines = 99
        elif self.difficulty.get() == 'Very Hard':
            self.rows = 30
            self.cols = 24
            self.mines = 160
            self.remainingMines = 160
            
    def reset(self):
        # resets the board and all attributes
        self.boardFrame.destroy()
        self.boardFrame = tk.Frame(self.master)
        self.boardFrame.grid(row=1, column=0)  
        self.firstClick = True    
        self.frames = {}
        self.flag = {}
        self.labels = {}
        self.revealed = {}
        self.minePlacement = {}
        self.invalidPlacement = {}
        
        # Reset stopwatch
        self.stopwatch.is_running = False
        self.stopwatch.start_time = 0
        self.stopwatch.elapsed_time = 0
        self.stopwatch.time_label.configure(text="00:00")
      
class StopwatchApp:
    def __init__(self, root):
        # Set up stopwatch widget
        self.root = root
        self.is_running = False
        self.start_time = 0
        self.elapsed_time = 0
        self.time_label = tk.Label(root, text="00:00", font=("Helvetica", 16))
        self.time_label.pack(pady=5)
        self.update()

    def start(self):
        # Start the stopwatch
        self.is_running = True
        self.start_time = time.time()
    
    def stop(self):
        # Stop the stopwatch
        self.is_running = False
        self.elapsed_time += time.time() - self.start_time

    def reset(self):
        # reset the stopwatch
        self.is_running = False
        self.elapsed_time = 0
        self.update()

    def update(self):
        # Update the visual stopwatch
        if self.is_running:
            elapsed = self.elapsed_time + (time.time() - self.start_time)
        else:
            elapsed = self.elapsed_time

        minutes = int(elapsed // 60)
        seconds = int(elapsed % 60)

        time_str = f"{minutes:02d}:{seconds:02d}"
        self.time_label.config(text=time_str)
        self.root.after(50, self.update)  # Update every 50 milliseconds
s
# initaite the class that runs the games
Minesweeper()