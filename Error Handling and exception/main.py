try:
    file = open("fab.txt")
except FileNotFoundError:
    print("file does not exist")

