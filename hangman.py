from pathlib import Path
HANGMAN_ASCII_ART = "welcome to the game hangman"
MAX_TRIES = 6
old_letters_guessed = []
num_of_tries = 1
secret_word = ""
HANGMAN_PHOTOS = {1: """
    x-------x
""", 2: """
    x-------x
    |
    |
    |
    |
    |
""", 3: """
    x-------x
    |       |
    |       0
    |
    |
    |
""", 4: """
    x-------x
    |       |
    |       0
    |       |
    |
    |
""", 5: """
    x-------x
    |       |
    |       0
    |      /|\\
    |
    |
""", 6: """
    x-------x
    |       |
    |       0
    |      /|\\
    |      /
    |
""", 7: """
    x-------x
    |       |
    |       0
    |      /|\\
    |      / \\
    |
"""}


def start():
    """prints name of game"""
    print(f"""
    {HANGMAN_ASCII_ART}\n\
    _    _
   | |  | |
   | |__| | __ _ _ __   __ _ _ __ ___   __ _ _ __
   |  __  |/ _' | '_ \ / _' | '_ ' _ \ / _' | '_ \\
   | |  | | (_| | | | | (_| | | | | | | (_| | | | |
   |_|  |_|\__,_|_| |_|\__, |_| |_| |_|\__,_|_| |_|
                        __/ |
                       |___/\
    \n{MAX_TRIES}
    """)


def is_valid_input(letter_guessed):
    """checks if guess is valid.
   :param letter_guessed: letter guess
   :type letter_guessed: string
   :return: validity of guess
   :rtype: bool
   """
    if(len(letter_guessed) > 1 or not letter_guessed.isalpha()):
        return False
    else:
        return True


def check_valid_input(letter_guessed, old_letters_guessed):
    """checks if guess is valid and not guessed before.
   :param letter_guessed: letter guess
   :param old_letters_guessed: list of letters guessed
   :type letter_guessed: string
   :type old_letters_guessed: list
   :return: validity of guess and if guess has been previously guessed
   :rtype: bool
   """
    if not is_valid_input(letter_guessed) or\
       letter_guessed in old_letters_guessed:
        return False
    else:
        return True


def try_update_letter_guessed(letter_guessed, old_letters_guessed):
    """if guess is valid and if not guessed before, adds guess to list of guesses.
    if guess invalid or guessed before, prints previous guesses
    sorted in lower case.
   :param letter_guessed: letter guess
   :param old_letters_guessed: list of letters guessed
   :type letter_guessed: string
   :type old_letters_guessed: list
   :return: validity of guess and if guess has been previously guessed
   :rtype: bool
   """
    if(check_valid_input(letter_guessed, old_letters_guessed)):
        old_letters_guessed.append(letter_guessed.lower())
        return True
    else:
        l = sorted(old_letters_guessed, key=str.lower)
        l = " -> ".join(l)
        print("X\n"+l)
        return False


def show_hidden_word(secret_word, old_letters_guessed):
    """shows letters in secret word that have been correctly guessed and the
    letters that haven't been guessed yet are shown as underlines
   :param secret_word: word to guess
   :param old_letters_guessed: list of letters guessed
   :type secret_word: string
   :type old_letters_guessed: list
   :return: how word currently looks
   :rtype: string
   """
    secret_word = secret_word.lower()
    str = ""
    for letter in secret_word:
        if letter in old_letters_guessed:
            str += letter + " "
        else:
            str += "_ "
    return str


def check_win(secret_word, old_letters_guessed):
    """checks if player won
   :param secret_word: word to guess
   :param old_letters_guessed: list of letters guessed
   :type secret_word: string
   :type old_letters_guessed: list
   :return: if player won or not
   :rtype: bool
   """
    for ch in show_hidden_word(secret_word, old_letters_guessed):
        if ch == "_":
            return False
    return True


def print_hangman(num_of_tries):
    """prints hangman photo corresponding to the current number of incorrect tries
   :param num_of_tries: number of incorrect guesses
   :type num_of_tries: int
   """
    if num_of_tries != 0:
        print(HANGMAN_PHOTOS[num_of_tries])


def choose_word(file_path, index):
    """chooses word to guess
   :param file_path: path of file of words
   :param index: index of word chosen
   :type file_path: string
   :type index: int
   :return: number of unique words in file and
   the word in the index chosen to guess
   :rtype: tuple
   """
    global secret_word
    f = open(file_path, "r")
    r = f.read()
    f.close()
    l = r.split(" ")
    if int(index) > len(l):
        n = int(index)-len(l)
        while n > len(l):
            n -= len(l)
        w = l[n-1]
    else:
        w = l[int(index)-1]
    t = (int(len(set(l))), w)
    secret_word = w
    return t


def main():
    global num_of_tries
    start()
    f = input("please enter file path of words: ")
    n = input("please enter index of word: ")
    my_file = Path(f)
    # checks if file path exists
    while not my_file.is_file():
        f = input("please enter existing file path of words: ")
        my_file = Path(f)
    choose_word(f,n)
    print("let's start!")
    print_hangman(num_of_tries)
    print(show_hidden_word(secret_word, old_letters_guessed))
    while not check_win(secret_word, old_letters_guessed) and\
            num_of_tries != 7:
        guess = input("Guess a letter: ")
        # if the letter guessed isn't in secret word, prints out hangman photo
        if (guess.lower() not in secret_word.lower()) and\
           (check_valid_input(guess, old_letters_guessed)):
            num_of_tries += 1
            print(":(")
            print_hangman(num_of_tries)
        resultofupdate = try_update_letter_guessed(guess, old_letters_guessed)
        resultofupdate
        if resultofupdate:
            print(show_hidden_word(secret_word, old_letters_guessed))
        if check_win(secret_word, old_letters_guessed):
            print("WIN")
        if num_of_tries == 7:
            print("LOSE")


if __name__ == "__main__":
    main()
