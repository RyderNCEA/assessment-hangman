import tkinter as tk
from tkinter import *
import random

# Page Object
class Page():
    def __init__(self, window):
        self.components = []
        self.frame = Frame(window, width=WINDOW_DIMENSIONS[0], height=WINDOW_DIMENSIONS[1], bg="#F9EBD1")

    # Add components to page
    def add_component(self, object, xpos, ypos, anchor, width, height):
        self.components.append([object,xpos,ypos, anchor, width, height])
        return

# Game Page Manager
class PageHandler():
    def __init__(self, home):
        self.current = home
    
    # Get the games current page frame
    def getPage(self):
        return self.current.frame

    # Change the games page
    def setPage(self, page):
        # Place all components in desired page
        for component in page.components:
            self.current = page
            print(component)
            object = component[0]
            object.place(x=component[1], y=component[2], anchor=component[3], width=component[4], height=component[5])
            self.current.frame.place(x=0,y=0)

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
            
WINDOW_DIMENSIONS = ['805','480']
center_anchor = [int(WINDOW_DIMENSIONS[0])/2 , int(WINDOW_DIMENSIONS[0])/2]
window = tk.Tk()

window.title("Hangman Game")
window.geometry('x'.join(WINDOW_DIMENSIONS))
window.configure(bg="#F9EBD1")

window.mainloop()
