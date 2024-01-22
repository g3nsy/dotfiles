import os
import json

home = os.path.expanduser('~')
here = os.path.dirname(os.path.relpath(__file__))
data_path = os.path.join(here, 'data.json')

with open(data_path, mode='r', encoding='UTF-8') as f:
    data = json.load(f)

    os.system(f'sudo pacman --needed -S {" ".join(data["proglist"])}')

    for cfile, dest in data['configs'].items():
        dest = os.path.join(home, dest)
        os.makedirs(dest, exist_ok=True)
        os.system(f'cp -rfv {os.path.join(here, cfile)} {dest}')
