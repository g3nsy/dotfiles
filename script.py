import os
import json
import shutil

home = os.path.expanduser("~")
here = os.path.dirname(os.path.relpath(__file__))
data_path = os.path.join(here, "data.json")
scripts = os.path.join(here, "scripts")
sh = os.path.join(scripts, "sh")

with open(data_path, mode="r", encoding="UTF-8") as f:
    data = json.load(f)

    os.system(f'sudo pacman --needed -S {" ".join(data["proglist"])}')

    if shutil.which("yay") is None:
        os.system(
            "git clone https://aur.archlinux.org/yay.git && cd yay && makepkg -si"
        )

    os.system(f'yay --needed -S {" ".join(data["aurproglist"])}')

    for cfile, dest in data["configs"].items():
        dest = os.path.join(home, dest)
        os.makedirs(dest, exist_ok=True)
        os.system(f"cp -rfv {os.path.join(here, cfile)} {dest}")

    os.makedirs(os.path.join(home, ".local/share/fonts"), exist_ok=True)
    os.system(
        f'unzip {os.path.join(here, "Hack.zip")} -d  {os.path.join(home, ".local/share/fonts")}'
    )
    os.system("fc-cache -fv")

    os.system("git clone https://github.com/tmux-plugins/tpm ~/.tmux/plugins/tpm")
    os.system("sudo pacman -R vim")
    os.system("sudo ln -sfv /usr/bin/nvim /usr/bin/vim")
    os.system(f"pip install {' '.join(data['pyglib'])}")


for sh_script in os.listdir(path=sh):
    os.system(
        f"cp -v {os.path.join(sh, sh_script)} {os.path.join(home, '.local/bin/')}"
    )
