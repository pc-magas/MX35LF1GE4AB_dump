from typing import IO
import os


def open_file(filename: str) -> IO:
    """
    Open a file for writing after verifying it is not a directory
    and is writable (or can be created).

    :param filename: Path to the file
    :return: Writable file object
    :raises IsADirectoryError: if the path is a directory
    :raises PermissionError: if file or parent directory is not writable
    """

    if(filename.strip() == ""):
        raise RuntimeError("File name should not be empty")

    filename = os.path.abspath(filename)

    if os.path.isdir(filename):
        raise IsADirectoryError(f"'{filename}' is a directory, expected a file path")

    if os.path.exists(filename):
        if not os.access(filename, os.W_OK):
            raise PermissionError(f"File '{filename}' exists and is not writable")
    else:
        parent_dir = os.path.dirname(filename) or "."
        if not os.access(parent_dir, os.W_OK):
            raise PermissionError(f"Parent directory '{parent_dir}' is not writable")

    return open(filename, "wb")
