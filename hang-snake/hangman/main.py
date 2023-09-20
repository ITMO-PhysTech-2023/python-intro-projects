from hangman import run
import re
def main():
    def create_secret():
        return 'capybara'

    SECRET = create_secret()
    dict_ = dict()
    run.fillDictionary(SECRET, dict_)
    while True:
        letter = input('Enter a letter: ')
        run.logic(letter, dict_)
    print(run.returnCurrState())
main()