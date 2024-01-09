from utils import save, load, wrong_input

def init_settings():
    if not load('difficulty'):
        default_settings = {
            'difficulty': 'm',
            'mode': 'r',
            'score': 0,
            'level': 0,
            'next_level': 1,
            'next_level_score': 5
        }
        for key, value in default_settings.items():
            save(key, value)

def get_difficulty():
    print('''
    Select the difficulty:
        - "e" for easy. (correct answer = 1pt, wrong answer = 0)
        - "m" for medium. (correct answer = 2pts, wrong answer = -1)
        - "h" for hard. (correct answer = 10pts, wrong answer = -5)
        choice: ''', end='')
    difficulty = input().lower()

    while difficulty not in ['e', 'm', 'h']:
        wrong_input()
        difficulty = input("Please choose a valid difficulty (e/m/h): ").lower()
    
    save('difficulty', difficulty)
    print(f'Difficulty set to {difficulty}.')

def reset_stats():
    save('score', 0)
    save('level', 0)
    save('next_level', 1)
    save('next_level_score', 5)
    print("Stats reset successfully.")
