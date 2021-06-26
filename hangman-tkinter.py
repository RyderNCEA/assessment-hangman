from tkinter import *
from tkmacosx import Button
import random

# COLOURS
darkgrey = '#2B2C2C'
beige = '#F9EBD1'
orange = '#FBBC52'

# Button Values
letters = "abcdefghijklmnopqrstuvwxyz"

# Window Dimensions
WINDOW_DIMENSIONS = ['805','480']
center_anchor = [int(WINDOW_DIMENSIONS[0])/2 , int(WINDOW_DIMENSIONS[0])/2]

# Page Object
class Page():
    def __init__(self, window):
        self.components = []
        self.frame = Frame(window, width=WINDOW_DIMENSIONS[0], height=WINDOW_DIMENSIONS[1], bg="#F9EBD1")

    # Add components to page
    def add_component(self, object, xpos, ypos, anchor, width=None, height=None, command=None):
        self.components.append([object,xpos,ypos, anchor, width, height, command])
        return

# Game Page Manager
class PageHandler():
    def __init__(self, open):
        self.current = open
    
    # Get the games current page frame
    def getPage(self):
        return self.current.frame

    # Change the games page
    def setPage(self, page):

        # Remove current page
        self.current.frame.pack_forget()
            
        # Place all components in desired page
        for component in page.components:
            object = component[0]
            try:
                object.configure(command=component[6])
            except:
                pass
            object.place(x=component[1], y=component[2], anchor=component[3], width=component[4], height=component[5])
        self.current = page
        page.frame.pack()

class Game():
    def __init__(self):
        self.word = []
        self.attempts = 6

    # Get a random word from word list text file based on its length
    def randomWord(word_length):
        with open("word_list.txt", "r") as words:
            dictionary = []
            lines = words.readlines()
            for line in lines:
                dictionary.append(line.replace("\n", ""))
        self.word = random.choice(dictionary)
        while len(word) != word_length:
            word = random.choice(dictionary)


# Creation of Game
window = Tk()

window.title("Hangman Game")
window.geometry('x'.join(WINDOW_DIMENSIONS))
window.configure(bg=beige)
game = Game(window)

# Create Pages for Game
home = Page(window)
help = Page(window)
difficulty = Page(window)

pages = [home, help, difficulty]

pageFrames = {
  "home": home.frame,
  "help": help.frame,
  "difficulty": difficulty.frame
}

# Create Page Handler for Game with starting window "home"
pagehandler = PageHandler(home)

# Home Page Components
title = Label(pageFrames['home'], fg="#2B2C2C", bg=beige, text="Hangman", font=("Arial", 60))
home.add_component(title, center_anchor[0], 90, "center")

play_button = Button(pageFrames['home'], text="Play", font=("Arial", 20), background=orange, fg=darkgrey, borderless=1, activebackground='#ffd285', focuscolor='#ffd285')
play_button.configure(command=lambda window=window: pagehandler.setPage(difficulty))
home.add_component(play_button, center_anchor[0], 190, "center", 250, 65)

help_button = Button(pageFrames['home'], text="How to Play", font=("Arial", 20), background=orange, fg=darkgrey, borderless=1, activebackground='#ffd285', focuscolor='#ffd285')
help_button.configure(command=lambda window=window: pagehandler.setPage(help))
home.add_component(help_button, center_anchor[0], 270, "center", 250, 65)

pagehandler.setPage(home)

# Help Page Components
title = Label(pageFrames['help'], fg="#2B2C2C", bg=beige, text="Hangman", font=("Arial", 60))
help.add_component(title, center_anchor[0], 90, "center")

howtoplay = Label(pageFrames['help'], fg="#2B2C2C", font=("Arial", 20), 
    text="""A random word with a specific length is selected.   
The length of the word will be based on the difficulty  
you select or the level you are on. If you choose to    
play the progressive mode each round of hangman 
gets progressively harder.  

If you have 6 incorret guesses you lose! With each  
wrong guess the hangman graphic will move closer to 
completion.

If you guess a letter in the word that letter will be   
    uncovered for you to see and help you solve the word.   """)
help.add_component(howtoplay, center_anchor[0], 280, "center")

quit_button = Button(pageFrames['help'], text="Exit", font=("Arial", 15), background=orange, fg=darkgrey, borderless=1, activebackground='#ffd285', focuscolor='#ffd285')
help.add_component(quit_button, 60, 40, "center", 80, 40, command=lambda : pagehandler.setPage(home))



window.mainloop()
