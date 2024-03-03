import subprocess as sp
import time


def is_hdmi_connected() -> bool:
    comm = sp.run("xrandr | grep HDMI", shell=True, stdout=-1, stderr=-1)
    return comm.stdout.decode().split()[1] == "connected"


def get_xscreens() -> list:
    comm = sp.run("xrandr", shell=True, stdout=-1, stderr=-1)
    return [
        x.split()[0]
        for x in comm.stdout.decode().split("\n")[1:]
        if x and not x.startswith(" ")
    ]


def handle_screens() -> None:
    var = True
    screens = get_xscreens()
    edp = screens[0]
    hdmi = screens[1]
    while True:

        if is_hdmi_connected() and var:
            sp.run(
                f"xrandr --output {hdmi} --primary --mode 1920x1080 "
                + f"--right-of {edp} --output {edp} --off",
                shell=True,
            )
            var = False

        elif not is_hdmi_connected() and not var:
            sp.run("xrandr --auto", shell=True)
            var = True

        time.sleep(5)


if __name__ == "__main__":
    handle_screens()
