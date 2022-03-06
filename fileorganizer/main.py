import os
import pathlib
import shutil
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


def organize_files(root: str, output_dir: str) -> Tuple[List[pathlib.Path], List[pathlib.Path]]:
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
    for file in found_files:
        fileinfo: FileInfo = FileInfo(orig_path=file)

        output = f"{fileinfo.datetimeinfo.month}-{fileinfo.datetimeinfo.year} Sicherung"
        # _out = pathlib.Path(root + os.sep + "copiedfiles" + os.sep + output)
        _out = pathlib.Path(output_dir + os.sep + output)
        if not _out.exists():
            os.mkdir(_out)

        dst_file_path = pathlib.Path(f"{_out}{os.sep}{file.name}")
        if not dst_file_path.exists():
            shutil.copy(file, _out)
            fileinfo.dst_path = dst_file_path
            copied_files.append(dst_file_path)

    return found_files, copied_files


def make_gui():
    layout: List[List[sG.Element]] = [
        [
            sG.FolderBrowse(button_text="Select a directory to find files in", key="-ROOT-"),
            sG.Input(readonly=True),
        ],
        [
            sG.FolderBrowse(button_text="Select a output directory", key="-OUTPUT-"),
            sG.Input(readonly=True),
        ],
        [
            sG.Button(button_text="Organize Files", key="-RUN-"),
        ],
    ]
    window: sG.Window = sG.Window(title=f"File Organizer", layout=layout, finalize=True, resizable=False)
    return window


def main():
    window = make_gui()
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
                found_files, copied_files = organize_files(root_dir, output_dir)
                sG.Popup(f"Found {len(found_files)} file(s) during search. \n"
                         f"Copied {len(copied_files)} file(s) to the specified destination folder "
                         f"{'(as they were not yet present)' if len(copied_files) > 0 else '(as they were already present)'}. ",
                         title="Finished!")
        else:
            print(event, values)

    window.close()


main()
