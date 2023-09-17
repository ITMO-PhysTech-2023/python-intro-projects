from common.util import clear_terminal


def create_secret():
    return 'capybara'


SECRET = create_secret()
n = len(SECRET)

FINAL_FIELD = r'''
   +----+
   |    |
   o    |
  /|\   |
  / \   |
_______/|\_
'''

# здесь мы наверное хотим иметь исходное поле
# и понимание, как оно меняется после каждого хода
FIELD = FINAL_FIELD

while True:
    # make a move!
    letter = input('Enter your guess: ')
    if ...:
        FIELD = ...  # если не угадали, то надо обновить поле
    else:
        ...  # мало ли, понадобится...

    clear_terminal()
    print(FIELD)
