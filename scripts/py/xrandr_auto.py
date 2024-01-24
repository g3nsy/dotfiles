import subprocess as sp
import i3smart_workspaces as i3sw


def main():
    if i3sw.is_HDMI_connected():
        screens = i3sw.get_xrandr_screens()
        edp = screens[0]
        hdmi = screens[1]
        sp.run(f"xrandr --output {hdmi} --primary --mode 1920x1080 " +
               f"--right-of {edp} --output {edp} --off",
               shell=True)


if __name__ == '__main__':
    main()
