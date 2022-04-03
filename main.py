import random
import pickle
import os

print('''Welcome to Mathathon 1.0 by Jean-Paul
---------------------------------''')


def resetStats():  # Resets the stats to their default values.
    save('difficulty', 'm'), save('mode', 'r'), save('score', 0), save('level', 0), save('nextLevel', 1), save(
        'nextLevelScore', 5)


def initiation():  # Creates an initial save file for the first time the program is run

    # Checks if the file 'saveFile.dat' exists.
    if not os.path.exists('saveFile.dat'):
        settings = {'difficulty': 'm', 'mode': 'r', 'score': 0, 'level': 0, 'nextLevel': 1, 'nextLevelScore': 5}

        # If it does not exist, create a new file named saveFile.dat and write the initial setting values in it.
        with open('saveFile.dat', 'wb') as f:
            pickle.dump(settings, f)


def save(name, value):  # Save updated settings in the saveFile.dat file.

    # Opens the saveFile.dat and loads the initial settings and changes their value.
    with open('saveFile.dat', 'rb') as f:
        data = pickle.load(f)
        data[f'{name}'] = value

    # Saves the changes to saveFile.dat
    with open('saveFile.dat', 'wb') as f:
        pickle.dump(data, f)


def load(name):  # Loads settings variables from saveFile.dat.
    with open('saveFile.dat', 'rb') as f:
        data = pickle.load(f)

        return data[f'{name}']


def getNumber():  # Generates a random number based on the difficulty chosen by the user.
    difficulty = load('difficulty')  # Loads the difficulty settings from the save file.

    # increases the range of the random numbers based on the difficulty set.
    if difficulty.lower() == 'e':
        number = random.randint(0, 10)
    elif difficulty.lower() == 'm':
        number = random.randint(0, 50)
    else:
        number = random.randint(0, 100)

    return number


def calculateScore(correctAnswers, wrongAnswers):  # Calculates the changes in score and then saves them.
    # Loads the variables from the save file.
    score, difficulty, level, nextLevel, nextLevelScore = load('score'), load('difficulty'), load('level'), load(
        'nextLevel'), load('nextLevelScore')

    # Calculate the score changes based on the difficulty and the number of correct and wrong answers.
    if difficulty == 'e':
        score += correctAnswers
    elif difficulty == 'm':
        score += (2 * correctAnswers - wrongAnswers)
    else:
        score += (10 * correctAnswers - 5 * wrongAnswers)

    # Checks if the user has accumulated enough score to get to the next level.
    while score >= nextLevelScore:
        save('score', score)
        levelUp()
        nextLevelScore = load('nextLevelScore')

    save('score', score)
    print(f'''
Difficulty: {load('difficulty')}.
Score: {load('score')}/{load('nextLevelScore')}.
Level {load('level')}.
Points till level {load('nextLevel')}: {load('nextLevelScore') - load('score')}''')


def validateInput(q):  # Validates the user input.
    while not q.isnumeric():
        wrongInput()
        q = input()

    return eval(q)


def generateRandomNumbers():
    # Generates random numbers
    n1 = getNumber()
    n2 = getNumber()

    # Puts the bigger number instead because in cause of subtraction,
    # First graders are too dumb to understand negative numbers
    if n2 > n1:
        n1, n2 = n2, n1

    return n1, n2


def correctAnswerChecker(correctAnswer, userAnswer):  # Checks if the answer is correct or not
    if correctAnswer == userAnswer:
        print('Correct answer!')
        print()
    else:
        print('Wrong answer!')
        print()
        print(f'Correct answer: {correctAnswer}.')
        print()
    return correctAnswer == userAnswer


def stats():  # Outputs the stats
    score, level, nextLevelScore = load('score'), load('level'), load('nextLevelScore')
    print(f'''
Level: {level}.
Score till next level: {score}/{nextLevelScore}
''')
    input('Press any key to go back to the main menu.')
    menu()


def levelUp():  # Checks if the user got enough score in order to level up
    level, nextLevel, nextLevelScore, score = load('level'), load('nextLevel'), load('nextLevelScore'), load('score')

    while score >= nextLevelScore:
        level += 1
        nextLevel += 1
        nextLevelScore *= 2
        save('level', level), save('nextLevel', nextLevel), save('nextLevelScore', nextLevelScore)

    print(f'''Congratulations! You just reached level {level}.''')


def wrongInput():
    print('Wrong input, try again.')


def getOperation():  # Prompts the user to choose an operation mode.
    op = {'a': 'addition', 's': 'subtraction', 'm': 'multiplication', 'd': 'division', 'r': 'random'}
    print('''
    Select modes:
    - "a" for Addition.
    - "s" for subtraction.
    - "m" for multiplication.
    - "d" for division.
    - "r" for a random choice.
    choice: ''', end='')
    answer = input().lower()

    if answer.lower() in 'asmdr':
        save('mode', f'{answer}')
        print(f'Mode set to {op[answer]}.')
    else:
        wrongInput()
        print()
        getOperation()


def getDifficulty():  # Prompts the user to choose a difficulty level.
    dif = {'e': 'easy', 'm': 'medium', 'h': 'hard'}
    print('''
    Select the difficulty:
        - "e" for easy. (correct answer = 1pt, wrong answer = 0)
        - "m" for medium. (correct answer = 2pts, wrong answer = -1)
        - "h" for hard. (correct answer = 10pts, wrong answer = -5)
        choice: ''', end='')
    answer = input().lower()

    # Validates input
    if answer.lower() in 'emh':
        save('difficulty', f'{answer}')
        print(f'Difficulty set to {dif[answer]}.')
        menu()

    wrongInput()
    print()
    getDifficulty()


def practice():  # Start the practice game mode. (no score is counted)
    play()
    menu()


def test():  # Starts the test game mode.
    correctAnswers, wrongAnswers = play()
    calculateScore(correctAnswers, wrongAnswers)
    menu()


def play():
    getOperation()
    questions = input('Enter the number of questions: ')

    questions = validateInput(questions)
    correctAnswers = 0
    wrongAnswers = 0
    difficulty, mode = load('difficulty'), load('mode')

    # Selects the operator based on the mode chosen
    if mode.lower() == 'a':
        operator = '+'
    elif mode.lower() == 's':
        operator = '-'
    elif mode.lower() == 'm':
        operator = '*'
    else:
        operator = '/'

    for x in range(questions):
        # if the mode is random the operator is randomly chosen every question.
        if mode.lower() == 'r':
            operator = random.choice(['+', '-', '*', '/'])
        n1, n2 = generateRandomNumbers()
        answer = eval(f'{n1}{operator}{n2}')

        # Writes 'x' instead of '*' and '÷' instead of '/'
        if operator == '*':
            userAnswer = input(f'{n1} × {n2} = ')
        elif operator == '/':
            userAnswer = input(f'{n1} ÷ {n2} = ')
        else:
            userAnswer = input(f'{n1} {operator} {n2} = ')

        userAnswer = validateInput(userAnswer)

        if correctAnswerChecker(answer, userAnswer):
            correctAnswers += 1
        else:
            wrongAnswers += 1

    print(f'You got {correctAnswers} correct answers out of {questions}')

    return correctAnswers, wrongAnswers


def playMenu():  # Outputs the play menu
    gameMode = input(f'''
Choose a game mode:
1- Practice. (Practice your maths skills without making level changes).
2- Test. (Test your math skills while leveling up).
3- To go back to the main menu
Choice: ''')

    while eval(gameMode) not in range(1, 4) or len(gameMode) != 1:
        wrongInput()
        gameMode = input()

    gameMode = eval(gameMode)

    if gameMode == 1:
        practice()
    elif gameMode == 2:
        test()
    else:
        menu()


def menu():  # Opens the main menu
    difficulty = load('difficulty')
    print(f'''
1- Play.
2- Change the difficulty (currently: {difficulty}).
3- Check your stats.
4- Reset your stats.
5- Exit the program.
choice: ''', end='')

    answer = input()

    # Validates input
    while not answer.isnumeric() or eval(answer) not in range(1, 6):
        wrongInput()
        answer = input()

    answer = eval(answer)

    if answer == 1:
        playMenu()
    elif answer == 2:
        getDifficulty()
    elif answer == 3:
        stats()
    elif answer == 4:
        answer = input('Are you sure you want to reset your stats? (Y/N) :')

        if answer.lower() == 'y':
            resetStats()
            print('Stats reset successfully.')
            menu()
        else:
            menu()
    else:
        exit()


def main():
    initiation()
    menu()


if __name__ == '__main__':
    main()
