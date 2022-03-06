import os
from dataclasses import dataclass
from pathlib import Path

from fileorganizer.utils.dateutils import CreatedAtDatetimeInfo


@dataclass(frozen=False)
class FileInfo:
    orig_path: Path  # in case we add functionality to redo the moving of files (e.g. not simply copying them anymore)
    datetimeinfo: CreatedAtDatetimeInfo
    dst_path: Path = None

    def __init__(self, orig_path):
        self.orig_path = orig_path
        self.datetimeinfo = CreatedAtDatetimeInfo(timestamp=os.stat(orig_path).st_ctime)
