import zipfile
from datetime import datetime
import yaml

history = []
path = ['archive']
directory = []
all_f = []


def clear():
    global history, all_f, path, directory
    history = []
    all_f = []
    path = ['archive']
    directory = []


def add_to_history(user, command, param):
    action = {
        "user": user,
        "command": command,
        "param": param,
        "time": str(datetime.now())
    }
    history.append(action)


def find_file(text):
    global path, directory
    if text[0] == '/':
        path_new = path + text[1:].split('/')
    else:
        path_new = text.split('/')
    for elem in directory:
        if elem == path_new:
            return elem
    return None


def rep(x):
    if x[-1] == '/':
        return x.split('/')[:-1]
    return x.split('/')


def head_file(archive, filepath, num_lines=10):
    """Reads the first `num_lines` of a file from the zip archive."""
    try:
        with archive.open(filepath, 'r') as file:
            for i, line in enumerate(file):
                if i >= num_lines:
                    break
                print(line.decode().strip())
    except KeyError:
        print(f"File '{filepath}' not found in archive.")
    except Exception as e:
        print(f"Error reading file '{filepath}': {e}")


def main_c():
    global path
    with open('konf.yaml') as f:
        templates = yaml.safe_load(f)

    files = templates['path_vm'] + "\\archive.zip"
    user = templates['user']
    computer = templates['computer']
    with zipfile.ZipFile(files) as zf:
        for der in sorted(map(rep, zf.namelist()), key=lambda x: len(x)):
            directory.append(der)

        while True:
            try:
                print(f"[{user}@{computer}] : {'/'.join(path)} :", end='')
                command, *param = input().split()
            except ValueError:
                continue

            add_to_history(user, command, param)

            if command == "ls":
                current_dir = '/'.join(path)
                content = [d[-1] for d in directory if d[:-1] == path]
                if content:
                    for item in content:
                        print(item)
                else:
                    print(f"No files in directory '{current_dir}'")

            elif command == "cd":
                if len(param) == 0:
                    print("You need to specify a directory")
                    continue
                file = find_file(param[0])
                if file is None:
                    print(f"Path '{param[0]}' does not exist.")
                else:
                    path = file

            elif command == "head":
                if len(param) == 0:
                    print("You need to specify a file.")
                    continue
                filepath = '/'.join(path + [param[0]])
                num_lines = int(param[1]) if len(param) > 1 else 10
                head_file(zf, filepath, num_lines)

            elif command == "history":
                for action in history:
                    print(action['time'], action['user'], action['command'], action['param'])

            elif command == "exit":
                break

            else:
                print(f"The name '{command}' is not recognized as a command name")


    clear()


if __name__ == '__main__':
    main_c()
