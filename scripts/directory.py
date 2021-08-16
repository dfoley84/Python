import os
from pathlib import Path

## Display all Directory paths including Sub Directory Folders
def top_down():
    for dirpath, dirnames, files in os.walk('C:\\'):
        print("Directory", dirpath)
        print("Sub directories")
        for dirname in dirnames:
            print(dirname)
        print("Including Files")
        for filename in files:
            print(filename)
        print()


def directory_contents():
    #entries = Path('C:\\')
    #entries = Path.home()
    entries = Path.cwd()

    for entry in entries.iterdir():
        print(entry.name)
        print(entry.parent)
        print(entry.parent.parent)
        print(entry.stem)
        print(entry.suffix)

def make_directory():
    try:
        os.mkdir("logs/")
    except FileExistsError as ex:
        print("Directory already exists")

def path_make_directory():
    dir_path = Path('logs/')
    dir_path.mkdir(exist_ok=True)


def count():
    total = 0
    for base, subdirs, files in os.walk('C:\\bin\\'):
        for file in files:
            total += 1
    return total 

if __name__ == "__main__":
    print(count())
