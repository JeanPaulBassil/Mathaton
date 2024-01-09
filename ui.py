from game_logic import practice, test
from settings import get_difficulty, reset_stats
from utils import load, wrong_input

def menu():
    while True:
        print(f'''
1- Play.
2- Change the difficulty (currently: {load('difficulty')}).
3- Check your stats.
4- Reset your stats.
5- Exit the program.
Choice: ''', end='')

        choice = input().strip()

        if choice == '1':
            play_menu()
        elif choice == '2':
            get_difficulty()
        elif choice == '3':
            stats()
        elif choice == '4':
            if confirm_reset():
                reset_stats()
        elif choice == '5':
            print("Exiting program. Goodbye!")
            break
        else:
            wrong_input()

def play_menu():
    while True:
        print(f'''
Choose a game mode:
1- Practice. (Practice your maths skills without making level changes).
2- Test. (Test your math skills while leveling up).
3- Go back to the main menu.
Choice: ''', end='')

        choice = input().strip()

        if choice == '1':
            practice()
        elif choice == '2':
            test()
        elif choice == '3':
            break
        else:
            wrong_input()

def stats():
    score, level, next_level_score = load('score'), load('level'), load('next_level_score')
    print(f'''
Level: {level}.
Score: {score}/{next_level_score}.
''')
    input("Press any key to go back to the main menu.")

def confirm_reset():
    answer = input("Are you sure you want to reset your stats? (Y/N): ").lower()
    return answer == 'y'
