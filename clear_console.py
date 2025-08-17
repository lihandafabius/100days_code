# clear_console.py
import os

def clear():
    # Check for the operating system and clear the console screen
    os.system('cls' if os.name == 'nt' else 'clear')
