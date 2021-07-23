# Problem Set 2, hangman.py
# Name: 
# Collaborators:
# Time spent:

# Hangman Game
# -----------------------------------
# Helper code
# You don't need to understand this helper code,
# but you will have to know how to use the functions
# (so be sure to read the docstrings!)
import random
import string

WORDLIST_FILENAME = "words.txt"


def load_words():
    """
    Returns a list of valid words. Words are strings of lowercase letters.
    
    Depending on the size of the word list, this function may
    take a while to finish.
    """
    print("Loading word list from file...")
    # inFile: file
    inFile = open(WORDLIST_FILENAME, 'r')
    # line: string
    line = inFile.readline()
    # wordlist: list of strings
    wordlist = line.split()
    print("  ", len(wordlist), "words loaded.")
    return wordlist


def choose_word(wordlist):
    """
    wordlist (list): list of words (strings)
    
    Returns a word from wordlist at random
    """
    return random.choice(wordlist)


# end of helper code

# -----------------------------------

# Load the list of words into the variable wordlist
# so that it can be accessed from anywhere in the program
wordlist = load_words()


def is_word_guessed(secret_word, letters_guessed):
    '''
    secret_word: string, the word the user is guessing; assumes all letters are
      lowercase
    letters_guessed: list (of letters), which letters have been guessed so far;
      assumes that all letters are lowercase
    returns: boolean, True if all the letters of secret_word are in letters_guessed;
      False otherwise
    '''
    correct_guess = 0
    # Check how many characters match
    for char in secret_word:
        if char in letters_guessed:
            correct_guess += 1
    # If every character match return True
    if correct_guess == len(secret_word):
        return True
    else:
        return False


def get_guessed_word(secret_word, letters_guessed):
    '''
    secret_word: string, the word the user is guessing
    letters_guessed: list (of letters), which letters have been guessed so far
    returns: string, comprised of letters, underscores (_), and spaces that represents
      which letters in secret_word have been guessed so far.
    '''
    guess_word = ""
    # Loop through the letters to see if it has been guessed
    for i in range(len(secret_word)):
        # Reveal it if it has been guessed
        if secret_word[i] in letters_guessed:
            guess_word += secret_word[i]
        # Else keep it as "_ "
        else:
            guess_word += "_ "
    return guess_word


def get_available_letters(letters_guessed):
    '''
    letters_guessed: list (of letters), which letters have been guessed so far
    returns: string (of letters), comprised of letters that represents which letters have not
      yet been guessed.
    '''
    available_letters = ""
    letter_list = string.ascii_lowercase
    # Loop for unused letters
    for char in letter_list:
        if char not in letters_guessed:
            available_letters += char
    return available_letters


def hangman(secret_word):
    '''
    secret_word: string, the secret word to guess.
    
    Starts up an interactive game of Hangman.
    
    * At the start of the game, let the user know how many 
      letters the secret_word contains and how many guesses s/he starts with.
      
    * The user should start with 6 guesses

    * Before each round, you should display to the user how many guesses
      s/he has left and the letters that the user has not yet guessed.
    
    * Ask the user to supply one guess per round. Remember to make
      sure that the user puts in a letter!
    
    * The user should receive feedback immediately after each guess 
      about whether their guess appears in the computer's word.

    * After each guess, you should display to the user the 
      partially guessed word so far.
    
    Follows the other limitations detailed in the problem write-up.
    '''
    print("Welcome to the game Hangman!")
    print(f"I am thinking of a word that is {len(secret_word)} letters long.")
    # Initializing the variables
    letters_guessed = []
    user_guess = 6
    warning = 3
    vowels = ["a", "e", "i", "o", "u"]
    unique_word = []
    for char in secret_word:
        if char not in unique_word:
            unique_word.append(char)
    # While loop until word is guessed or user ran out of guess chance
    while not is_word_guessed(secret_word, letters_guessed) and user_guess > 0:
        print("---------------")
        print(f"You have {user_guess} guesses left.")
        print("Available letters:", get_available_letters(letters_guessed))
        guess = input("Please guess a letter:")
        # Check if its a valid letter
        if guess.isalpha():
            guess.lower()
            # Check for repeated letters
            if guess in letters_guessed:
                if warning > 0:
                    print("Oops You've already guessed that letter")
                    warning -= 1
                    print(f"You now have {warning} warnings left.")
                else:
                    user_guess -= 1
            else:
                if guess in secret_word:
                    print("Good guess")
                else:
                    print("Oops That letter is not in my word")
                    user_guess -= 1
                    if guess in vowels:
                        user_guess -= 1
                letters_guessed.append(guess)
            print(get_guessed_word(secret_word, letters_guessed))
        else:
            warning -= 1
            print(f"Oops that is not a valid letter,you have {warning} warnings left.")
    # End of game(Lost)
    if user_guess <= 0:
        print(f"Sorry,you ran out of guesses,the word is {secret_word}")
    # End of Game(Win)
    else:
        score = len(unique_word) * user_guess
        print("Congratulations,you won!")
        print("your total score for this game is: ", score)


# -----------------------------------


def match_with_gaps(my_word, other_word):
    '''
    my_word: string with _ characters, current guess of secret word
    other_word: string, regular English word
    returns: boolean, True if all the actual letters of my_word match the 
        corresponding letters of other_word, or the letter is the special symbol
        _ , and my_word and other_word are of the same length;
        False otherwise: 
    '''
    # Initializing variables
    letter_list = []
    error = 0
    match = 0
    requirement = 0
    # Removing the space in-between "_"
    guessed_word = my_word.replace(" ", "")
    for char in guessed_word:
        if char not in letter_list and char.isalpha():
            letter_list.append(char)
    # Check for length
    if len(other_word) == len(guessed_word):
        for i in range(len(guessed_word)):
            # Making sure every letter match
            if guessed_word[i].isalpha():
                requirement += 1
                if guessed_word[i] == other_word[i]:
                    match += 1
            else:
                if other_word[i] in letter_list:
                    error += 1
    if error == 0 and match == requirement and requirement > 0:
        return True
    else:
        return False


def show_possible_matches(my_word):
    '''
    my_word: string with _ characters, current guess of secret word
    returns: nothing, but should print out every word in wordlist that matches my_word
             Keep in mind that in hangman when a letter is guessed, all the positions
             at which that letter occurs in the secret word are revealed.
             Therefore, the hidden letter(_ ) cannot be one of the letters in the word
             that has already been revealed.

    '''
    possible_match = ""
    for words in wordlist:
        if match_with_gaps(my_word, words):
            possible_match += " " + words
    if possible_match == "":
        print("No matches found")
    else:
        print(possible_match)


def hangman_with_hints(secret_word):
    '''
    secret_word: string, the secret word to guess.
    
    Starts up an interactive game of Hangman.
    
    * At the start of the game, let the user know how many 
      letters the secret_word contains and how many guesses s/he starts with.
      
    * The user should start with 6 guesses
    
    * Before each round, you should display to the user how many guesses
      s/he has left and the letters that the user has not yet guessed.
    
    * Ask the user to supply one guess per round. Make sure to check that the user guesses a letter
      
    * The user should receive feedback immediately after each guess 
      about whether their guess appears in the computer's word.

    * After each guess, you should display to the user the 
      partially guessed word so far.
      
    * If the guess is the symbol *, print out all words in wordlist that
      matches the current guessed word. 
    
    Follows the other limitations detailed in the problem write-up.
    '''
    print("Welcome to the game Hangman!")
    print(f"I am thinking of a word that is {len(secret_word)} letters long.")
    # Initializing the variables
    letters_guessed = []
    user_guess = 6
    warning = 3
    vowels = ["a", "e", "i", "o", "u"]
    unique_word = []
    for char in secret_word:
        if char not in unique_word:
            unique_word.append(char)
    while not is_word_guessed(secret_word, letters_guessed) and user_guess > 0:
        print("---------------")
        print(f"You have {user_guess} guesses left.")
        print("Available letters:", get_available_letters(letters_guessed))
        guess = input("Please guess a letter:")
        if guess.isalpha():
            guess.lower()
            # Check if letter is repeated
            if guess in letters_guessed:
                if warning > 0:
                    print("Oops You've already guessed that letter")
                    warning -= 1
                    print(f"You now have {warning} warnings left.")
                else:
                    user_guess -= 1
            else:
                if guess in secret_word:
                    print("Good guess")
                else:
                    print("Oops That letter is not in my word")
                    user_guess -= 1
                    if guess in vowels:
                        user_guess -= 1
                letters_guessed.append(guess)
            print(get_guessed_word(secret_word, letters_guessed))
        else:
            # Special Move!
            if guess == "*":
                show_possible_matches(get_guessed_word(secret_word, letters_guessed))
            else:
                warning -= 1
                print(f"Oops that is not a valid letter,you have {warning} warnings left.")
    # End of game(Lose!)
    if user_guess <= 0:
        print(f"Sorry,you ran out of guesses,the word is {secret_word}")
    # End of game(Win!)
    else:
        score = len(unique_word) * user_guess
        print("Congratulations,you won!")
        print("your total score for this game is: ", score)

if __name__ == "__main__":

    # To test part 2, comment out the pass line above and
    # uncomment the following two lines.
    #secret_word = choose_word(wordlist)
    #hangman(secret_word)

    ###############

    # To test part 3 re-comment out the above lines and 
    # uncomment the following two lines.
    secret_word = choose_word(wordlist)
    hangman_with_hints(secret_word)
