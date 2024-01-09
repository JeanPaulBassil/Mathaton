import pickle
import os

def save(name, value):
    if os.path.exists('saveFile.dat'):
        with open('saveFile.dat', 'rb') as f:
            data = pickle.load(f)
    else:
        data = {}
    data[name] = value
    with open('saveFile.dat', 'wb') as f:
        pickle.dump(data, f)

def load(name):
    if not os.path.exists('saveFile.dat'):
        return None
    with open('saveFile.dat', 'rb') as f:
        data = pickle.load(f)
    return data.get(name)

def validate_input(input_str):
    while not input_str.isnumeric():
        wrong_input()
        input_str = input("Please enter a valid number: ")
    return int(input_str)

def wrong_input():
    print("Invalid input. Please try again.")
