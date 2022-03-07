import os
import pathlib
import shutil
import threading
import time
from typing import Tuple, List

import PySimpleGUI as sG

from fileorganizer.utils import FileInfo

# not case-sensitive for path.glob(), but otherwise yes
glob_file_extension_patterns: Tuple = ("*.png", "*.PNG",
                                       "*.jpg", "*.JPG", "*.jpeg", "*.JPEG",
                                       "*.mp3", "*.MP3", "*.mp4", "*.MP4", "*.m4a", "*.M4A")
file_extension_patterns: Tuple = (".png", ".PNG",
                                  ".jpg", ".JPG", ".jpeg", ".JPEG",
                                  ".mp3", ".MP3", ".mp4", ".MP4", ".m4a", ".M4A")


organize_finished_event = "-ORGANIZE FINISHED-"


def organize_files(window: sG.Window, root: str, output_dir: str) -> None:  # -> Tuple[List[pathlib.Path], List[pathlib.Path]]:
    found_files: List[pathlib.Path] = []
    copied_files: List[pathlib.Path] = []
    # for rootdir, dirnames, filenames in os.walk(u"C:\\Users\\Naraka\\PycharmProjects\\file-organizer"):
    for rootdir, dirnames, filenames in os.walk(root):
        # print(rootdir)
        # print(dirnames)
        # print(filenames)

        # only works, obviously, when there are directories involved, otherwise it won't find anything
        # (e.g. at the root level on start it won't find any files)
        # though we could circumvent this by simply using the parent of the first root,
        # but this ma not be desired as then other directories/files could be copied over
        # which were not part of the original directory structure
        # for dirname in dirnames:
        #     path = pathlib.Path(os.path.join(root, dirname))
        #     for pattern in patterns:
        #         found_image_files = path.glob(pattern=pattern)
        #         found_files.extend(found_image_files)

        for file in filenames:
            f_path = pathlib.Path(os.path.join(root, file))
            if f_path.suffix in file_extension_patterns:
                found_files.append(f_path)

    print(f"Found {len(found_files)} file(s) matching the given patterns {glob_file_extension_patterns}:")
    print(found_files)

    # TODO: update progressbar here, as we know how many files we have found
    for file in found_files:
        fileinfo: FileInfo = FileInfo(orig_path=file)

        output = f"{fileinfo.datetimeinfo.created_at.month}-{fileinfo.datetimeinfo.created_at.year} Sicherung"
        # _out = pathlib.Path(root + os.sep + "copiedfiles" + os.sep + output)
        _out = pathlib.Path(output_dir + os.sep + output)
        if not _out.exists():
            os.mkdir(_out)

        dst_file_path = pathlib.Path(f"{_out}{os.sep}{file.name}")
        if not dst_file_path.exists():
            shutil.copy(file, _out)
            fileinfo.dst_path = dst_file_path
            copied_files.append(dst_file_path)

    window.write_event_value("-ORGANIZE FINISHED-", (found_files, copied_files))


def progress(thread: threading.Thread, window: sG.Window) -> None:
    # https://github.com/PySimpleGUI/PySimpleGUI/issues/535
    window["-PROGRESS BAR-"].update(bar_color=("white", "green"), visible=True)
    while thread.is_alive():
        window["-PROGRESS BAR-"].Widget["value"] += window["-PROGRESS BAR-"].metadata
        time.sleep(0.1)
    window["-PROGRESS BAR-"].update(bar_color=("white", "green"))


def make_gui():
    layout: List[List[sG.Element]] = [
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
            sG.HorizontalSeparator(pad=((5, 5), (10, 10))),
        ],
        [
            sG.Button(button_text="Organize Files", key="-RUN-"),
            sG.ProgressBar(max_value=100, size=(30, 10), key="-PROGRESS BAR-", metadata=25, visible=False, border_width=2),
        ],
    ]
    window: sG.Window = sG.Window(title=f"File Organizer", layout=layout, finalize=True, resizable=False)
    return window


def main():
    sG.theme("Material2")
    window = make_gui()
    # https://github.com/PySimpleGUI/PySimpleGUI/issues/2599
    window["-PROGRESS BAR-"].Widget.config(mode="indeterminate")
    while True:
        event, values = window.read()
        if event == sG.WINDOW_CLOSED or event == "Quit":
            break
        elif event == "-RUN-":
            root_dir: str = values["-ROOT-"]
            output_dir: str = values["-OUTPUT-"]
            print(root_dir, output_dir)
            print(event, values)
            if not root_dir == output_dir:
                # new thread to search for files
                organize_thread: threading.Thread = threading.Thread(target=organize_files,
                                                                     args=(window, root_dir, output_dir,),
                                                                     daemon=True)
                organize_thread.start()
                # thread to show progress bar until above thread is working
                threading.Thread(target=progress, args=(organize_thread, window), daemon=True).start()
        elif event == organize_finished_event:
            found_files, copied_files = values[event]
            sG.Popup(f"Found {len(found_files)} file(s) during search. \n"
                     f"Copied {len(copied_files)} file(s) to the specified destination folder "
                     f"{'(as they were not yet present)' if len(copied_files) > 0 else '(as they were already present)'}. ",
                     title="Finished!")
        else:
            print(event, values)

    window.close()


main()
