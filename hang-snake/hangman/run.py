while True:
    from random import *
    from WORDS import listOfWords
    from HANGMAN import *
    playerChances = len(hangmanStages)
    falseChoices = 0
    openedLetters = []
    word = choice(listOfWords)
    zagadka = '_' * len(word)
    while falseChoices < playerChances and zagadka != word:
        print(hangmanStages[falseChoices])
        print(zagadka)
        print('\n Введите предполагаемую РУССКУЮ букву:')
        x = input()
        if len(x) != 1:
            print('\n Неправильный ввод!!! Просили же одну букву....')
            break
        if ord(x) > ord('я') or ord(x) < ord('а'):
            print('\n Неправильный ввод!!! Просили же русскую букву....')
        else:
            while x in openedLetters:
                print('\n Ты же уже пытался...')
                x = input()
            openedLetters.append(x)
            if x in word:
                print('\n Угадал? Странно')
                finalWord = ''
                for i in range(len(word)):
                    if x == word[i]:
                        finalWord += x
                    else:
                        finalWord += zagadka[i]
                zagadka = finalWord
            else:
                print('\n Не угадал)')
                falseChoices += 1
    if falseChoices == playerChances:
        print(hangmanStages[falseChoices])
        print("\nТебя повесили!")
    else:
        if '_' in zagadka:
            print("\nТы проиграл, так как назвал несколько букв сразу")
        else:
            print("\nТы угадал слово")

    print("\nЗагаданное слово было \"" + word + '\"')
