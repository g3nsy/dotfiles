import psutil  # type: ignore
import os


def is_tmux_running():
    for process in psutil.process_iter(['pid', 'name']):
        if 'tmux' in process.info['name']:  # type: ignore
            return True
    return False


if __name__ == "__main__":
    os.system(f'alacritty --command tmux {"attach" if is_tmux_running() else ""}')
