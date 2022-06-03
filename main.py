import os
import pathlib
import shutil
import threading
from typing import Tuple, List, Callable

import PySimpleGUI as sG

from fileorganizer.utils import FileInfo
from fileorganizer.gui.gui import make_gui


# not case-sensitive for path.glob(), but otherwise yes
glob_file_extension_patterns: Tuple = ("*.png", "*.PNG",
                                       "*.jpg", "*.JPG", "*.jpeg", "*.JPEG",
                                       "*.mp3", "*.MP3", "*.mp4", "*.MP4", "*.m4a", "*.M4A")
file_extension_patterns: Tuple = (".png", ".PNG",
                                  ".jpg", ".JPG", ".jpeg", ".JPEG",
                                  ".mp3", ".MP3", ".mp4", ".MP4", ".m4a", ".M4A")


ORGANIZE_FINISHED_EVENT = "-ORGANIZE FINISHED-"


def organize_files(window: sG.Window, root: str, output_dir: str, is_move_files_selected: bool) -> None:
    found_files: List[pathlib.Path] = []
    copied_files: List[pathlib.Path] = []
    for rootdir, dirnames, filenames in os.walk(root):
        for file in filenames:
            f_path = pathlib.Path(os.path.join(rootdir, file))
            if f_path.suffix in file_extension_patterns:
                found_files.append(f_path)

    shutil_copy_or_move: Callable = shutil.move if is_move_files_selected else shutil.copy
    # https://github.com/PySimpleGUI/PySimpleGUI/issues/4659 ...
    window["-PROGRESS BAR-"].update(0, bar_color=("black", "white"), visible=True, max=len(found_files))
    for file in found_files:
        fileinfo: FileInfo = FileInfo(orig_path=file)

        output = f"{fileinfo.datetimeinfo.created_at.month}-{fileinfo.datetimeinfo.created_at.year} Sicherung"
        # _out = pathlib.Path(root + os.sep + "copiedfiles" + os.sep + output)
        _out = pathlib.Path(output_dir + os.sep + output)
        if not _out.exists():
            os.mkdir(_out)

        dst_file_path = pathlib.Path(f"{_out}{os.sep}{file.name}")
        if not dst_file_path.exists():
            shutil_copy_or_move(file, _out)
            fileinfo.dst_path = dst_file_path
            copied_files.append(dst_file_path)

        window["-PROGRESS BAR-"].Widget["value"] += window["-PROGRESS BAR-"].metadata

    window.write_event_value("-ORGANIZE FINISHED-", (found_files, copied_files))


def main():
    sG.theme("Material2")
    window = make_gui()
    # https://github.com/PySimpleGUI/PySimpleGUI/issues/2599
    # window["-PROGRESS BAR-"].Widget.config(mode="indeterminate")
    while True:
        event, values = window.read()
        if event == sG.WINDOW_CLOSED or event == "Quit":
            break
        elif event == "-RUN-":
            root_dir: str = values["-ROOT-"]
            output_dir: str = values["-OUTPUT-"]
            if not root_dir or not output_dir:
                sG.Popup("Both directories need to be selected!", title="Error")
                continue
            if root_dir == output_dir:
                sG.Popup("Both directories cannot be the same!", title="Error")
                continue

            is_move_files_selected = values["-MOVE FILES-"]
            # new thread to search for files
            organize_thread: threading.Thread = threading.Thread(target=organize_files,
                                                                 args=(window,
                                                                       root_dir,
                                                                       output_dir,
                                                                       is_move_files_selected,),
                                                                 daemon=True)
            organize_thread.start()
        elif event == ORGANIZE_FINISHED_EVENT:
            found_files, copied_files = values[event]
            is_move_files_selected = values["-MOVE FILES-"]
            sG.Popup(f"Found {len(found_files)} file(s) during search. \n"
                     f"{'Copied' if not is_move_files_selected else 'Moved'} {len(copied_files)} file(s) to the specified destination folder "
                     f"{'(as they were not yet present)' if len(copied_files) > 0 else '(as they were already present)'}. ",
                     title="Finished!")
            window["-PROGRESS BAR-"].update(visible=False)

    window.close()


if __name__ == '__main__':
    main()
