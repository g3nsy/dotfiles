import i3ipc
import subprocess as sp
import time
import xrandr_auto
import threading
import logging


logger = logging.getLogger(__name__)


def is_HDMI_connected() -> bool:
    comm = sp.run("xrandr | grep HDMI", shell=True, stdout=-1, stderr=-1)
    return comm.stdout.decode().split()[1] == "connected"


def get_xrandr_screens() -> list:
    comm = sp.run("xrandr", shell=True, stdout=-1, stderr=-1)
    return [
        x.split()[0]
        for x in comm.stdout.decode().split("\n")[1:]
        if x and not x.startswith(" ")
    ]


def get_workspaces_by(i3: i3ipc.connection.Connection, screen: str) -> list:
    return [x for x in i3.get_workspaces() if x.ipc_data["output"] == screen]


def move_workspaces_to(
    i3: i3ipc.connection.Connection, workspaces: list, direction: str
) -> None:
    for w in workspaces:
        i3.command(f"workspace {w.num}")
        i3.command(f"move workspace to output {direction}")


def is_workspace_empty(
    i3: i3ipc.connection.Connection, workspace: i3ipc.replies.WorkspaceReply
) -> bool:
    workspace = i3.get_tree().find_by_id(workspace.ipc_data["id"])
    return not workspace or not workspace.workspace().leaves()


def handler_function(
    i3: i3ipc.connection.Connection,
    i3thread: threading.Thread,
    sec: int = 5,
    direction_HDMI: str = "left",
    direction_PRIMARY: str = "right",
) -> None:
    HDMI = get_xrandr_screens()[1]
    left_move = not is_HDMI_connected()
    right_move = left_move
    HDMI_workspaces = None
    while True:
        if not i3thread.is_alive():
            break
        HDMI_connected = is_HDMI_connected()
        if not HDMI_connected and not left_move:
            HDMI_workspaces = get_workspaces_by(i3, HDMI)
            move_workspaces_to(i3, HDMI_workspaces, direction_HDMI)
            sp.run("xrandr --auto", shell=True)
            right_move = False
            left_move = True
        if HDMI_connected and HDMI_workspaces and not right_move:
            xrandr_auto.main()
            move_workspaces_to(
                i3,
                [x for x in HDMI_workspaces if not is_workspace_empty(i3, x)],
                direction_PRIMARY,
            )
            time.sleep(3)
            i3.command("restart")
            right_move = True
            left_move = False
        time.sleep(sec)


def main():
    while True:
        i3 = i3ipc.Connection()
        thread = threading.Thread(target=i3.main, args=[])
        thread.start()
        handler_function(i3, thread)


if __name__ == "__main__":
    main()
