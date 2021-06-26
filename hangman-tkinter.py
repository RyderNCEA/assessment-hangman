import tkinter as tk
from tkinter import *
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


window = tk.Tk()

window.title("Hangman Game")
window.geometry('x'.join(WINDOW_DIMENSIONS))
window.configure(bg="#F9EBD1")

game = Game()
home = Page(window)
help = Page(window)

pagehandler = PageHandler(home)
frame = pagehandler.getPage()

# Universal Components
title = Label(frame, fg="#2B2C2C", bg="#F9EBD1", text="Hangman", font=("Arial", 60))

# Home Page Components
play_button = Button(frame, text="Play", font=("Arial", 20), highlightbackground="#FBBC52", fg="#2B2C2C", highlightthickness=60, width=230, height=50)
#play_button.configure(command=lambda window=window: pageManager(window, "difficulty"))

help_button = Button(frame, text="How to Play", font=("Arial", 20), highlightbackground="#FBBC52", fg="#2B2C2C", highlightthickness=60)
help_button.configure(command=lambda window=window: pagehandler.setPage(help))

home.add_component(title, center_anchor[0], 80, "center", None, None)
home.add_component(help_button, center_anchor[0], 240, "center", 230, 50)
home.add_component(play_button, center_anchor[0], 170, "center", 230, 50)
pagehandler.setPage(home)

help.add_component(title, center_anchor[0], 80, "center", None, None)


window.mainloop()
