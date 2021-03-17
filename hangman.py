import random

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
