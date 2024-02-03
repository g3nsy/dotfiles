import os
import json
import shutil


HOME = os.path.expanduser("~")
HERE = os.path.dirname(os.path.relpath(__file__))
DATA = os.path.join(HERE, "data.json")
SCRIPTS = os.path.join(HERE, "scripts")
SH_SCRIPTS = os.path.join(SCRIPTS, "sh")


with open(DATA, mode="r", encoding="UTF-8") as f:
    data = json.load(f)


def install_scripts() -> None:
    for sh_script in os.listdir(path=SH_SCRIPTS):
        os.system(
            f"cp -v {os.path.join(SH_SCRIPTS, sh_script)} {os.path.join(HOME, '.local/bin/')}"
        )


def install_theme() -> None:
    theme_path = os.path.join(HOME, "theme")
    for file in ["cursor.tar.gz", "icons.tar.xz", "theme.tar.xz"]:
        os.system(
            f"sudo tar -v -xf {os.path.join(theme_path, file)} -C /usr/share/icons/"
        )


def install_programs() -> None:
    os.system(f'sudo pacman --needed -S {" ".join(data["proglist"])}')

    if shutil.which("yay") is None:
        os.system(
            "git clone https://aur.archlinux.org/yay.git && cd yay && makepkg -si"
        )

    os.system(f'yay --needed -S {" ".join(data["aurproglist"])}')


def install_configs() -> None:
    for cfile, dest in data["configs"].items():
        dest = os.path.join(HOME, dest)
        os.makedirs(dest, exist_ok=True)
        os.system(f"cp -rfv {os.path.join(HERE, cfile)} {dest}")


def install_fonts() -> None:
    os.makedirs(os.path.join(HOME, ".local/share/fonts"), exist_ok=True)
    fonts_dir = os.path.join(HERE, "fonts")
    for font in data["fonts"]:
        os.system(
            f'unzip -o {os.path.join(fonts_dir, font)} -d  {os.path.join(HOME, ".local/share/fonts")}'
        )
    os.system("fc-cache -fv")


def do_tmux_required_operation():
    os.system("git clone https://github.com/tmux-plugins/tpm ~/.tmux/plugins/tpm")


def do_extra_operations():
    os.system("sudo pacman -R vim")
    os.system("sudo ln -sfv /usr/bin/nvim /usr/bin/vim")


def install_pylibs() -> None:
    os.system(f"pip install {' '.join(data['pyglib'])}")


def main() -> None:
    install_programs()
    install_scripts()
    install_configs()
    install_theme()
    install_fonts()
    install_pylibs()
    do_tmux_required_operation()
    do_extra_operations()


if __name__ == "__main__":
    main()
