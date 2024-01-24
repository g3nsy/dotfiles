import os
import json

home = os.path.expanduser("~")
here = os.path.dirname(os.path.relpath(__file__))
data_path = os.path.join(here, "data.json")
scripts = os.path.join(here, "scripts")
sh = os.path.join(scripts, "sh")

with open(data_path, mode="r", encoding="UTF-8") as f:
    data = json.load(f)

    os.system(f'sudo pacman --needed -S {" ".join(data["proglist"])}')

    for cfile, dest in data["configs"].items():
        dest = os.path.join(home, dest)
        os.makedirs(dest, exist_ok=True)
        os.system(f"cp -rfv {os.path.join(here, cfile)} {dest}")

for sh_script in os.listdir(path=sh):
    os.system(
        f"cp -v {os.path.join(sh, sh_script)} {os.path.join(home, '.local/bin/')}"
    )
