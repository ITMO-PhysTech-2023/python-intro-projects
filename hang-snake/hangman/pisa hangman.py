from random import choice
plate = (
    """
            +
            |
            |   
            |
            |
    _______/|\\_
    """,
    """
       +----+
       |    |
            |
            |
            |
    _______/|\\_
    """,
    """
       +----+
       |    |
       o    |
            |
            |
    _______/|\\_
    """,
    """
       +----+
       |    |
       o    |
      /|\\   |
            |
    _______/|\\_
    """,
    """
       +----+
       |    |
       o    |
      /|\\   |
      / \\
    _______/|\\_
    """
)
mistakes = len(plate)
words = ('машина', 'слон', 'мегафакультет', 'баратрум', 'контейнер', 'пылесос', 'капибара', 'снитч')
word = choice(words)
wordlist = list(word)
print(word)
word1 = []
for i in range(len(word)):
    word1.append('-')
wrong = 0
while mistakes != 0 and word1 != word:
    letter = input('Дай мне букву: ')
    if letter in word:
        a = ''
        for i in range(len(word)):
            if letter == word[i]:
                a += letter
            else:
                a += word1[i]
        word1 = a
    else:
        mistakes = mistakes - 1
        wrong += 1
    print(word1)
    if mistakes == 0:
        print('лузер!')
        print(plate[4])
        break
    else:
        print(plate[wrong])
print('ну лан')