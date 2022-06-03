from dataclasses import dataclass
from pathlib import Path

from fileorganizer.utils.dateutils import DatetimeInfo


@dataclass(frozen=False)
class FileInfo:
    """ Represents some information about the supplied file.

        Each FileInfo instance consists of:

        - the `orig_path` of the file

        - the `datetimeinfo` (when the file was created/modified, etc.)

        - the `dst_path` of the file, to know where the new file path lies
            -> (useful once a "revert" functionality has been implemented)
    """

    orig_path: Path  # in case we add functionality to redo the moving of files (e.g. not simply copying them anymore)
    datetimeinfo: DatetimeInfo
    dst_path: Path = None

    def __init__(self, orig_path):
        self.orig_path = orig_path
        self.datetimeinfo = DatetimeInfo(path=orig_path)
