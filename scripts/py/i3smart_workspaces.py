import subprocess as sp
import time
import xrandr_auto
import logging
from threading import Thread
from i3ipc.connection import Connection   # type: ignore
from i3ipc.replies import WorkspaceReply  # type: ignore


logger = logging.getLogger(__name__)


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


def get_workspaces_by(i3con: Connection, screen: str) -> list:
    return [x for x in i3con.get_workspaces() if x.ipc_data["output"] == screen]


def move_workspaces_to(
    i3con: Connection, workspaces: list, direction: str
) -> None:
    for w in workspaces:
        i3con.command(f"workspace {w.num}")
        i3con.command(f"move workspace to output {direction}")


def is_workspace_empty(
    i3con: Connection, wkrepy: WorkspaceReply
) -> bool:
    wktarget = i3con.get_tree().find_by_id(wkrepy.ipc_data["id"])
    return not wktarget or not wktarget.workspace().leaves()  # type: ignore


def handler_function(
    i3con: Connection,
    i3main_thread: Thread,
    sleep_time: int = 5,
    hdmi_direction: str = "left",
    primary_direction: str = "right"
) -> None:
    hdmi_id = get_xscreens()[1]
    left_move = not is_hdmi_connected()
    right_move = left_move
    hdmi_workspaces = None
    while True:
        # i3 reloaded, let's quit and relaunch this 
        if not i3main_thread.is_alive():
            break

        hdmi_connected = is_hdmi_connected()

        if not hdmi_connected and not left_move:
            hdmi_workspaces = get_workspaces_by(i3con, hdmi_id)
            move_workspaces_to(i3con, hdmi_workspaces, hdmi_direction)
            sp.run("xrandr --auto", shell=True)
            right_move, left_move = (False, True)

        if hdmi_connected and hdmi_workspaces and not right_move:
            xrandr_auto.main()
            move_workspaces_to(i3con, [x for x in hdmi_workspaces if not is_workspace_empty(i3con, x)], primary_direction)
            time.sleep(3)
            i3con.command("restart")
            right_move, left_move = (True, False)

        time.sleep(sleep_time)


def main():
    while True:
        i3con = Connection()
        i3main_thread = Thread(target=i3con.main, args=[])
        i3main_thread.start()
        handler_function(i3con, i3main_thread)


if __name__ == "__main__":
    main()
