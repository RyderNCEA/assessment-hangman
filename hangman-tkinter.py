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
        self.frame = Frame(window, width=WINDOW_DIMENSIONS[0], height=WINDOW_DIMENSIONS[1], bg=beige)

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
    def __init__(self, window):
        self.word = []
        self.progress = []
        self.window = window
        self.attempts = 6
        self.game_difficulty = 4
        self.progressive = False
        self.graphic = PhotoImage(file="images/graphic7.png")
    # Get a random word from word list text file based on its length
    def randomWord(self, word_length):
        with open("word_list.txt", "r") as words:
            dictionary = []
            lines = words.readlines()
            for line in lines:
                dictionary.append(line.replace("\n", ""))
        self.word = random.choice(dictionary)
        while len(self.word) != word_length:
            self.word = random.choice(dictionary)

    # Set the difficulty of the game 
    def set_difficulty(self, difficulty):
        if type(difficulty) == str and "Progressive" == difficulty:
            self.progressive = True
            game_difficulty = 4
        else:
            game_difficulty = difficulty
            self.progressive = False
        return game_difficulty

    # Check if a users guess is correct or incorrect
    def guess(self, button, word, progress, progresslabel, graphic, pagehandler, endpage):
        guess = button.cget('text')
        word = word.upper()
        for letter in word:
            if guess == letter:
                # Gather all occurences of letter
                occurences = [i for i in range(len(word)) if word.find(guess, i) == i]
                # Add each occurence to what the user has solved so far
                for occurence in occurences:
                    progress[occurence] = guess
                # Update the word
                progresslabel.configure(text=" ".join(progress))
                button.place_forget()
                # Check if user has guessed the full word
                if(word == "".join(progress)):
                    pagehandler.setPage(endpage)
                    endpage.components[1][0].configure(text="You Win!")
                return
        self.attempts -= 1
        button.place_forget()
        # Check if user has run out of attempts
        if(self.attempts == 0):
            endpage.components[1][0].configure(text="You Lose!")
            self.graphic = PhotoImage(file="images/graphic7.png")
            graphic.configure(image=self.graphic)
            pagehandler.setPage(endpage)
        self.graphic = PhotoImage(file="images/graphic{}.png".format(str(self.attempts+1)))
        graphic.configure(image=self.graphic)
        return

    # Start round of game
    def start_round(self, mode, ph, window):
        self.progress = []
        self.attempts = 6
        self.graphic = PhotoImage(file="images/graphic7.png")
        self.randomWord(mode)

        # End Page
        endpage = Page(window)
        endpage_frame = endpage.frame
        title = Label(endpage_frame, fg=darkgrey, bg=beige, text="Hangman", font=("Arial", 60))
        endpage.add_component(title, center_anchor[0], 90, "center")
        subtitle = Label(endpage_frame, bg=orange, fg=darkgrey, text="You {}!", font=("Arial", 40))
        endpage.add_component(subtitle, center_anchor[0], 160, "center")
        play_button = Button(endpage_frame, font=("Arial", 20), background=orange, fg=darkgrey, borderless=1, activebackground='#ffd285', focuscolor='#ffd285')
        exit_button = Button(endpage_frame, text="Menu", font=("Arial", 20), command=lambda window=window: ph.setPage(home), background=orange, fg=darkgrey, borderless=1, activebackground='#ffd285', focuscolor='#ffd285')
        if self.progressive == True and mode != 11:
            self.game_difficulty += 1
            play_button.configure(command=lambda window=window: self.start_round(self.game_difficulty, ph, window), 
            text="Next Round")
        else:
            play_button.configure(command=lambda window=window: pagehandler.setPage(difficulty), 
            text="Play Again")
        endpage.add_component(play_button, center_anchor[0], 230, "center", 250, 65)
        endpage.add_component(exit_button, center_anchor[0], 300, "center", 250, 65)

        # Game Page
        roundpage = Page(window)
        roundpage_frame = roundpage.frame
        graphic_canvas = Label(roundpage_frame, image=self.graphic, bg=beige)
        roundpage.add_component(graphic_canvas, 140, 30, None, width=120,height=156)
        for i in range(len(self.word)): self.progress.append("_")
        word_display = Label(roundpage_frame, fg=darkgrey, bg=beige, text=" ".join(self.progress), font=("Arial", 50))
        roundpage.add_component(word_display, center_anchor[0]+100, 90, "center")
        quit_button = Button(roundpage_frame, text="Exit", font=("Arial", 15), background=orange, fg=darkgrey, borderless=1, activebackground='#ffd285', focuscolor='#ffd285')
        roundpage.add_component(quit_button, 60, 40, "center", 80, 40, command=lambda : pagehandler.setPage(home))
        xpos = 25
        ypos = 220
        for l in letters:
            if l == "j" or l == "s":
                ypos += 85
                if l == "s":
                    xpos = 68
                else:
                    xpos = 25
            letter_button = Button(roundpage_frame, text=l.upper(), font=("Arial", 20), focuscolor='#ffd285', activebackground="#ffd894",bg=orange, fg=darkgrey)
            roundpage.add_component(letter_button, xpos, ypos, None, width=70, height=70, command=lambda object=letter_button: self.guess(object,self.word,self.progress,word_display, graphic_canvas, ph, endpage))
            xpos += 85
        ph.setPage(roundpage)
        

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
title = Label(pageFrames['home'], fg=darkgrey, bg=beige, text="Hangman", font=("Arial", 60))
home.add_component(title, center_anchor[0], 90, "center")

play_button = Button(pageFrames['home'], text="Play", font=("Arial", 20), background=orange, fg=darkgrey, borderless=1, activebackground='#ffd285', focuscolor='#ffd285')
play_button.configure(command=lambda window=window: pagehandler.setPage(difficulty))
home.add_component(play_button, center_anchor[0], 190, "center", 250, 65)

help_button = Button(pageFrames['home'], text="How to Play", font=("Arial", 20), background=orange, fg=darkgrey, borderless=1, activebackground='#ffd285', focuscolor='#ffd285')
help_button.configure(command=lambda window=window: pagehandler.setPage(help))
home.add_component(help_button, center_anchor[0], 270, "center", 250, 65)

pagehandler.setPage(home)

# Help Page Components
title = Label(pageFrames['help'], fg=darkgrey, bg=beige, text="Hangman", font=("Arial", 60))
help.add_component(title, center_anchor[0], 90, "center")

howtoplay = Label(pageFrames['help'], fg=darkgrey, font=("Arial", 20), 
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

# Difficulty Page Components
title = Label(pageFrames['difficulty'], fg=darkgrey, bg=beige, text="Hangman", font=("Arial", 60))
difficulty.add_component(title, center_anchor[0], 90, "center")

subtitle = Label(pageFrames['difficulty'], fg=darkgrey, bg=beige, text="Select your game difficulty:", font=("Arial", 30))
difficulty.add_component(subtitle, center_anchor[0], 160, "center")

temp_x = 85
temp_y = 190
# Add all dificulty buttons
for difficulty_level in range(4,12):
    play_button = Button(pageFrames['difficulty'], text=str(difficulty_level), font=("Arial", 20), background=orange, fg=darkgrey, borderless=1, activebackground='#ffd285', focuscolor='#ffd285')
    difficulty.add_component(play_button, temp_x, temp_y, None, 70, 70,command=lambda d=difficulty_level: game.start_round(game.set_difficulty(d), pagehandler, window))
    temp_x += 80

# Add progressive mode button
progressive_mode = Button(pageFrames['difficulty'], text="Progressive Mode", font=("Arial", 20), background=orange, fg=darkgrey, borderless=1, activebackground='#ffd285', focuscolor='#ffd285')
progressive_mode.configure(command=lambda d="Progressive": game.start_round(game.set_difficulty(d), pagehandler, window))
difficulty.add_component(progressive_mode, center_anchor[0], 320, "center", 190, 55)
window.mainloop()
