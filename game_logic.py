import random
from utils import save, load, validate_input, wrong_input

def get_number():
    difficulty = load('difficulty')
    if difficulty == 'e':
        return random.randint(0, 10)
    elif difficulty == 'm':
        return random.randint(0, 50)
    else:
        return random.randint(0, 100)

def calculate_score(correct_answers, wrong_answers):
    score, difficulty, level, next_level, next_level_score = load('score'), load('difficulty'), load('level'), load('next_level'), load('next_level_score')
    if difficulty == 'e':
        score += correct_answers
    elif difficulty == 'm':
        score += (2 * correct_answers - wrong_answers)
    else:
        score += (10 * correct_answers - 5 * wrong_answers)

    while score >= next_level_score:
        level_up()
        next_level_score = load('next_level_score')
    save('score', score)

def correct_answer_checker(correct_answer, user_answer):
    if correct_answer == user_answer:
        print('Correct answer!\n')
    else:
        print(f'Wrong answer!\nCorrect answer: {correct_answer}.\n')
    return correct_answer == user_answer

def level_up():
    level, next_level, next_level_score = load('level'), load('next_level'), load('next_level_score')
    level += 1
    next_level += 1
    next_level_score *= 2
    save('level', level)
    save('next_level', next_level)
    save('next_level_score', next_level_score)
    print(f'Congratulations! You just reached level {level}.')

def generate_random_numbers():
    n1, n2 = get_number(), get_number()
    if n2 > n1:
        n1, n2 = n2, n1
    return n1, n2

def play():
    mode = load('mode')
    questions = int(input('Enter the number of questions: '))
    correct_answers = 0
    wrong_answers = 0

    for _ in range(questions):
        operator = random.choice(['+', '-', '*', '/']) if mode == 'r' else {'a': '+', 's': '-', 'm': '*', 'd': '/'}[mode]
        n1, n2 = generate_random_numbers()
        answer = eval(f'{n1}{operator}{n2}')

        user_answer = validate_input(input(f'{n1} {"×" if operator == "*" else "÷" if operator == "/" else operator} {n2} = '))
        if correct_answer_checker(answer, user_answer):
            correct_answers += 1
        else:
            wrong_answers += 1

    print(f'You got {correct_answers} correct answers out of {questions}')
    return correct_answers, wrong_answers

def practice():
    play()
    # Add any additional practice-specific logic here if needed

def test():
    correct_answers, wrong_answers = play()
    calculate_score(correct_answers, wrong_answers)
