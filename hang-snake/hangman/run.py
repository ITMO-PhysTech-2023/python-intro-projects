from common.util import clear_terminal, HANGMAN_FIELDS
from common.hangman import Hangman
from common.words import choice_word

# здесь мы наверное хотим иметь исходное поле
# и понимание, как оно меняется после каждого хода
FIELD = HANGMAN_FIELDS[0]

hg = Hangman(choice_word())
while True:
    # make a move!
    letter = input('Enter your guess: ')[0]
    if not hg.guess(letter):
        FIELD = HANGMAN_FIELDS[hg.fails]
    if hg.fails == len(HANGMAN_FIELDS)-1:
        exit(1)
    clear_terminal()
    print(FIELD)
    print("Word", hg.get_partial_word())
    # TODO:
    if hg.get_partial_word() == hg.word:
        print("you won!!1!")
        exit(0)
