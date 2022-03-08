import threading
import time
from typing import List

import PySimpleGUI as sG


def progress(organize_thread: threading.Thread, window: sG.Window) -> None:
    # https://github.com/PySimpleGUI/PySimpleGUI/issues/535
    window["-PROGRESS BAR-"].update(bar_color=("white", "green"), visible=True)
    while organize_thread.is_alive():
        window["-PROGRESS BAR-"].Widget["value"] += window["-PROGRESS BAR-"].metadata
        time.sleep(0.1)
    window["-PROGRESS BAR-"].update(bar_color=("white", "green"))


def make_gui():
    layout: List[List[sG.Element]] = [
        [
            sG.Text(text="Organize your files (.png, .jpeg, .jpg, .mp3, .mp4, .m4a)\n"
                         "in a 'MONTH-YEAR' folder structure.\n"
                         "This program will (per default) COPY the files into the output directory.\n"
                         "The checkbox below will MOVE the files to the target location.")
        ],
        [
            sG.FolderBrowse(button_text="Select directory with files", key="-ROOT-"),
            sG.Push(),
            sG.Input(readonly=True, text_color="blue"),
        ],
        [
            sG.FolderBrowse(button_text="Select output directory", key="-OUTPUT-"),
            sG.Push(),
            sG.Input(readonly=True, text_color="blue"),
        ],
        [
            sG.Checkbox(text="MOVE files to the output directory?", key="-MOVE FILES-"),
        ],
        [
            sG.HorizontalSeparator(pad=((5, 5), (10, 10))),
        ],
        [
            sG.Button(button_text="Organize Files", key="-RUN-"),
            sG.ProgressBar(max_value=1, size=(30, 10), key="-PROGRESS BAR-", metadata=1, visible=False, border_width=2),
        ],
    ]
    window: sG.Window = sG.Window(title=f"File Organizer", layout=layout, finalize=True, resizable=False)
    return window
