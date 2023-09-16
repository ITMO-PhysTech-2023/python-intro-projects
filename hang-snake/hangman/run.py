from common.util import clear_terminal
class StaticVar:
    START_NUM = 0
def create_secret():
        return 'capybara'

SECRET = create_secret()
n = len(SECRET)

# здесь мы наверное хотим иметь исходное поле
# и понимание, как оно меняется после каждого хода

ZERO_STATE = r''''''
FIRST_STATE = r'''





    _______/|\_
    '''
SECOND_STATE = r'''

            |
            |
            |
            |
    _______/|\_
    '''
THIRD_STATE = r'''
       +----+
            |
            |
            |
            |
    _______/|\_
    '''
FORTH_STATE = r'''
       +----+
       |    |
            |
            |
            |
    _______/|\_
    '''
FINAL_STATE = r'''
       +----+
       |    |
       o    |
      /|\   |
      / \   |
    _______/|\_
    '''

state = [ZERO_STATE, FIRST_STATE, SECOND_STATE, THIRD_STATE, FORTH_STATE, FINAL_STATE]

# Создаём мапу из исходного слова и добавляем в неё каждую букву строки
dict = dict()
def fillDictionary(string, dict):
    for i in SECRET:
        if i not in dict:
            dict[i] = 1
        else:
            dict[i] += 1


def logic(letter, dict_):
    if letter in dict_:
        dict_.pop(letter)
    else:
        StaticVar.START_NUM += 1
    returnCurrState()
    if StaticVar.START_NUM == 5:
        exit(1)
    if len(dict_) == 0:
        print("YOU WIN!!!")
        exit(0)


def returnCurrState():
    print(state[StaticVar.START_NUM])

    # while True:
    # make a move!
    # letter = input('Enter your guess: ')
    # f ...:
    #    FIELD = ...  # если не угадали, то надо обновить поле
    # else:
    #    ...  # мало ли, понадобится...

    #clear_terminal()
    #print(FIELD)

