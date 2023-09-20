from hangman import StaticVar as sv
def create_secret():
        return 'capybara'

def fillDictionary(string, dict):
    for i in string:
        if i not in dict:
            dict[i] = 1
        else:
            dict[i] += 1


def returnCurrState():
    print(state[sv.StaticVar.START_NUM])

list_ = list()
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

def logic(letter, dict_):
    if letter in dict_:
        dict_.pop(letter)
    else:
        sv.StaticVar.START_NUM += 1
    returnCurrState()
    list_.append(letter)
    print("Already input characters: ")
    for i in list_:
         print(i + " ", end = ' ')
    print()
    if sv.StaticVar.START_NUM == 5:
        print("YOU LOSE!!!")
        exit(1)
    if len(dict_) == 0:
        print("YOU WIN!!!")
        exit(0)

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
