import random
import os
import time

# Terminal Colours
CBLUE = "\033[94m"
CGREEN = "\033[92m"
CRED = "\033[91m"
CEND = "\033[0m"

LETTERS = "ABCDEFGHIJKLMNOPQRSTUVWXYZ"

TITLE = """
--------------------------------------
  _  _                                
 | || |__ _ _ _  __ _ _ __  __ _ _ _  
 | __ / _` | ' \/ _` | '  \/ _` | ' \ 
 |_||_\__,_|_||_\__, |_|_|_\__,_|_||_|
                |___/                 
--------------------------------------                     
"""

# How many guesses to show each line
GUESSES_PER_LINE = 5

# Clear the users terminal
def clear():
    os.system('cls' if os.name == 'nt' else 'clear')

# Keep asking user question until answer is valid
def askUser(question, valid_inputs):
    while True:
        response = input(question)
        try:
            response = int(response)
        except:
            response = response.upper()
            
        for correct in valid_inputs:
            if response == correct:
                return response
            else:
                continue
        print("Invalid Input: input must be a valid input.")

# Load list of words from word_list.txt file
def get_dictionary():
    with open("word_list.txt", "r") as words:
        dictionary = []
        lines = words.readlines()
        for line in lines:
            dictionary.append(line.replace("\n", ""))
        return dictionary

# Get a word from word list based on its length
def get_word(word_length):
    dictionary = get_dictionary()
    word = random.choice(dictionary)
    while len(word) != word_length:
        word = random.choice(dictionary)
    return word

# Get specified hangman graphic from hangman_graphics.txt
def get_graphic(value):
    graphic = []
    lines_to_read = [lines for lines in range(8*value-8, 8*value)]
    with open("hangman_graphics.txt") as graphics:
        for position, line in enumerate(graphics):
            if position in lines_to_read:
                graphic.append(line.replace("\n",""))
        return graphic

# Check the users guess if it has any occurences in the word 
def guess(user_guess, solved, word):
    user_guess = user_guess.upper()
    word = word.upper()
    for letter in word:
        if user_guess == letter:
            # Gather all occurences of letter
            occurences = [i for i in range(len(word)) if word.find(user_guess, i) == i]
            # Add each occurence to what the user has solved so far
            for occurence in occurences:
                solved[occurence] = user_guess
            print("You guessed '{}' and it was {}correct{}!".format(user_guess, CGREEN, CEND))
            return [solved, True]
    print("You guessed '{}' and it was {}incorrect{}!".format(user_guess, CRED, CEND))
    return [solved, False]

# Update the game progress
def update_game(word, guesses, attempts):
    # Get the Hangman graphic based on remaining attempts
    graphic = get_graphic(attempts)
    # Display hidden word in form of "_ _ _ _" and show what is solved
    graphic[1] += "\t " + " ".join(word)
    # Display users guesses so far
    graphic[3] += "\t Your Guesses: "
    # Divide list of guesses into lines of 5 
    guesses = [guesses[x:x+GUESSES_PER_LINE] for x in range(0, len(guesses), GUESSES_PER_LINE)]
    for position in range(0, len(guesses)):
        if position+3 == 3:
            graphic[position+3] += ", ".join(guesses[position])
        else:
            graphic[position+3] += "\t " + ", ".join(guesses[position])
    # Print full game graphic
    print(TITLE)
    for line in graphic:
        print(line)
        
# Start the game of Hangman
def start_game():
    attempt = 1
    guesses = []
    progress = []
    print(TITLE)
    user_input = askUser("\nHave you played Hangman before? [Y]es or [N]o: ", ["YES","NO","Y","N"])
    clear()
    print(TITLE)
    print("""
    How to Play
    
    A random word with a specific length is selected.
    The length of the word will be based on the difficulty 
    you select or the level you are on if you choose to
    play the progressive mode where each round of hangman
    gets progressively harder.

    If you have 6 incorret guesses you lose! With each
    wrong guess the hangman graphic will move closer to
    completion.

    If you guess a letter in the word that letter will be
    uncovered for you to see and help you solve the word.""")

    user_input = askUser("\nPlease pick a difficulty [4 to 11] or [p]rogressive mode: ", ["PROGRESSIVE","P",4,5,6,7,8,9,10,11])
