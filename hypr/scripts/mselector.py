import subprocess as sp


def is_hdmi_connected() -> bool:
    try:
        rs = sp.check_output("xrandr | grep HDMI", shell=True).decode()
    except sp.CalledProcessError:
        return False
    return rs.split()[1] == "connected"


def set_monitors() -> None:
    if is_hdmi_connected():
        sp.run("hyprctl keyword monitor eDP-1, disable", shell=True)
        sp.run("hyprctl keyword HDMI-A-1, 1920x1080@60, 0x0, 1", shell=True)
    else:
        sp.run("hyprctl keyword monitor eDP-1, 1920x1080@60, 0x0, 1", shell=True)


if __name__ == "__main__":
    set_monitors()
