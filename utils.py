import random

def get_word():
    with open("words.txt", "r") as f:
        word_list = f.readlines()

        word = random.choice(word_list)
        word = word.strip()
        letters = [letter.lower() for letter in word]

    return letters

def is_valid_word(word):
    with open('sgb-words.txt', 'r') as f:
        word_list = f.readlines()
        word_list = [word.strip() for word in word_list]

    if word not in word_list:
        return False
    else:
        return True
