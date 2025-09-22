# Problem Set 2, hangman.py
# DUO's version

import random
import string

# -----------------------------------
# HELPER CODE
# -----------------------------------

WORDLIST_FILENAME = "words.txt"

def load_words():
    """
    returns: list, a list of valid words. Words are strings of lowercase letters.

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
    print(" ", len(wordlist), "words loaded.")
    return wordlist

def choose_word(wordlist):
    """
    wordlist (list): list of words (strings)

    returns: a word from wordlist at random
    """
    return random.choice(wordlist)


# -----------------------------------
# END OF HELPER CODE
# -----------------------------------


# Load the list of words to be accessed from anywhere in the program
wordlist = load_words()

def has_player_won(secret_word, letters_guessed):
    """
    secret_word: string, the lowercase word the user is guessing
    letters_guessed: list (of lowercase letters), the letters that have been
        guessed so far

    returns: boolean, True if all the letters of secret_word are in letters_guessed,
        False otherwise
    """
    for e in secret_word:
        if e not in letters_guessed:
            return False
    return True


def get_word_progress(secret_word, letters_guessed):
    """
    secret_word: string, the lowercase word the user is guessing
    letters_guessed: list (of lowercase letters), the letters that have been
        guessed so far

    returns: string, comprised of letters and asterisks (*) that represents
        which letters in secret_word have not been guessed so far
    """
    my_str = ""
    for e in secret_word:
        if e in letters_guessed:
            my_str += e
        else:
            my_str += "*"
    return my_str


def get_available_letters(letters_guessed):
    """
    letters_guessed: list (of lowercase letters), the letters that have been
        guessed so far

    returns: string, comprised of letters that represents which
        letters have not yet been guessed. The letters should be returned in
        alphabetical order
    """
    alphabet = string.ascii_lowercase
    the_available = ""
    for e in alphabet:
        if e not in letters_guessed:
            the_available += e
    return the_available


def reveal_letter(secret_word, letters_guessed):
    """
    secret_word: string, the lowercase word the user is guessing
    letters_guessed: list (of lowercase letters), the letters that have been
        guessed so far

    returns: string, comprised of a letter picked randomly from
        both the secret word and the available letters. 
    """
    available_letters = get_available_letters(letters_guessed)
    
    choose_from = ""
    for e in secret_word:
        if e in available_letters and e not in choose_from:
            choose_from += e
    
    new = random.randint(0, len(choose_from)-1)
    revealed_letter = choose_from[new]
    return revealed_letter


def hangman(secret_word, with_help):
    """
    * At the start, let the user know how many
      letters the secret_word contains and how many guesses they start with.

    * The user should start with 10 guesses.

    * Before each round, you should show how many guesses
      they have left and the letters that the user has not yet guessed.

    * Ask the user to supply one guess per round. Remember to make
      sure that the user puts in a single letter (or help character '!'
      for with_help functionality)

    * If the user inputs an incorrect consonant, then the user loses ONE guess,
      while if the user inputs an incorrect vowel (a, e, i, o, u),
      then the user loses TWO guesses.

    * The user should receive feedback immediately after each guess
      about whether their guess appears in the computer's word.

    * After each guess, you should display to the user the
      partially guessed word so far.

    -----------------------------------
    with_help functionality
    -----------------------------------
    * If the guess is the symbol !, you should reveal to the user one of the
      letters missing from the word at the cost of 3 guesses. If the user does
      not have 3 guesses remaining, print a warning message. Otherwise, add
      this letter to their guessed word and continue playing normally.

    """
    letters_guessed = ""
    
    unique_letters = ""
    for e in secret_word:
        if e not in unique_letters:
            unique_letters += e
    num_unique = len(unique_letters)

    difficulty = str(input('difficulty: 1.Easy/2.Standard/3.Hard? Plz press 1/2/3: '))
    if difficulty == '1':
        guesses = len(secret_word)*3
    elif difficulty == '2':
        guesses = round(len(secret_word)*2)
    else:
        guesses = len(secret_word)*1
    
    while guesses > 0 and not has_player_won(secret_word, letters_guessed):
        print("--------------")
        print(f"You have {guesses} lives left.")
        print(f"Available letters: {get_available_letters(letters_guessed)}")
        
        user_input = input("Please guess a letter: ").lower()
        if len(user_input) == 1:
            if with_help and user_input == "!":
                if guesses < 3:
                    print(f"Oops! Not enough lives: {get_word_progress(secret_word, letters_guessed)}")
                else:
                    guesses -= 3
                    reveal_this_time = reveal_letter(secret_word, letters_guessed)
                    letters_guessed += reveal_this_time
                    print(f"Letter revealed: {reveal_this_time}")
                    print(get_word_progress(secret_word, letters_guessed))
            elif user_input.isalpha():
                if user_input in letters_guessed:
                    print(f"Oops! Already guessed: {get_word_progress(secret_word, letters_guessed)}")
                else:
                    if user_input in secret_word:
                        letters_guessed += user_input
                        print(f"Good guess: {get_word_progress(secret_word, letters_guessed)}")
                    else:               
                        if user_input in "aeiou":
                            if guesses >= 2:
                                letters_guessed += user_input
                                guesses -= 2
                                print(f"Oops! Not in my word: {get_word_progress(secret_word, letters_guessed)}")
                            else:
                                print(f"Oops! Not enough lives: {get_word_progress(secret_word, letters_guessed)}")
                        else:
                            letters_guessed += user_input
                            guesses -= 1
                            print(f"Oops! Not in my word: {get_word_progress(secret_word, letters_guessed)}")
            else:
                print(f"Oops! Unvalid letter. Please input a letter from the alphabet: {get_word_progress(secret_word, letters_guessed)}")
        else:
            print(f"Oops! Unvalid letter. Please input a letter from the alphabet: {get_word_progress(secret_word, letters_guessed)}")
    if not has_player_won(secret_word, letters_guessed):
        print("--------------")
        print("Sorry, you ran out of guesses. The word was:", secret_word)
        print("You can press F5 for another round!")
    else:
        print("--------------")
        print("HOOOOOOOOOOOORAAAAAAAAAAAAY!")
        print("Congratulations, you won!!!")
        total_score = guesses + num_unique * 4 + len(secret_word) * 3
        #print(f"Your total score for this game is {total_score} :)")
        print("You can press F5 for another round!")

if __name__ == "__main__":

    secret_word = choose_word(wordlist)
    with_help = False

    print("Welcome to Hangman, an engaging word-guessing game!")
    print(f"I am thinking of a word that is {len(secret_word)} letters long.")
    print("When you guess correctly, there's no expense")
    print("When you guess wrongly, if you guess a vowel(a,e,i,o,u), the expense is 2 lives; otherwise, the expense is 1 life.")
    
    print('Help mode: when you press "!", a letter of the secret word is revealed, at the expense of 3 lives.')
    help_mode = str(input("Help mode(on/off): "))
    if help_mode.lower() == "on":
        with_help = True
    hangman(secret_word, with_help)