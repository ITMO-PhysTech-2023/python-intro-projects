from common.util import clear_terminal



def create_secret():
    return 'солнышко'
word = create_secret()

FIELD = (
    """
              
              
              
              
              
     _______/|\_ 
    """,
    """
              
              
              
             |
             |
     _______/|\_ 
    """,
    """
              
             |
             |
             |
             |
     _______/|\_ 
    """,
    """
       +-----+
             |
             |
             |
             |
     _______/|\_ 
    """,
    """
       +-----+
       |     |
             |
             |
             |
     _______/|\_ 
    """,
    """
       +-----+ 
       |     |
       o     |
             |
             |
     _______/|\_ 
    """,
    """
       +-----+
       |     |
       o     |
       |     |
             |
     _______/|\_ 
    """,
    """
       +-----+
       |     |
       o     |
      /|     |
             |
     _______/|\_ 
    """,
    """
       +-----+
       |     |
       o     |
      /|\    |
             |
     _______/|\_ 
    """,
    """
       +-----+
       |     |
       o     |
      /|\    |
      /      |
     _______/|\_ 
    """,
    """
       +-----+
       |     |
       o     |
      /|\    |
      / \    |
     _______/|\_ 
    """
)
number_of_errors = 0 #кол-во ошибок сделанных игроком
maximum_erorrs = 10 #максимальное количество ошибок
n = len(word)
guessed = ['_' for _ in range(n)] #угаданные
print(''.join(guessed))

while guessed != word and number_of_errors < maximum_erorrs:
    print('Enter your guess: ')# make a move!
    letter = input() #игрок вводит букву
    if letter in word:
        new = ""
        for i in range(len(word)): #ищем место буквы в слове
            if letter == word[i]:
                new += letter
            else:
                new += guessed[i]
        guessed = new
        print(''.join(guessed))
        print(FIELD[number_of_errors])
    else:
        print(('There is no such letter in word.'))
        number_of_errors +=1
        print(''.join(guessed))
        print(FIELD[number_of_errors])

if number_of_errors == maximum_erorrs:
    print(FIELD[number_of_errors])
    print("Game over")
else:
    print("Congratulations!The word was", word)

    clear_terminal()

