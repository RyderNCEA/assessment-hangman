import random

# Load list of words from word_list.txt file
def get_dictionary():
    with open("word_list.txt", "r") as words:
        dictionary = []
        lines = words.readlines()
        for line in lines:
            dictionary.append(line.replace("\n", ""))
        return dictionary
