import hashlib
import os

from six import string_types


def get_home_dir():
    """
    Returns the home directory of the current user.

    This is a best guess and may fail to achieve the real objective
    in exotic scenarios.
    """
    return os.path.expanduser("~")


def file_sha256(file_path):
    """
    Returns the hex representation of the SHA256 hash of file.

    The data is read in chunks to accommodate large files.
    """
    assert(isinstance(file_path, string_types))

    def read_in_chunks(file_object, chunk_size=1024):
        while True:
            data = file_object.read(chunk_size)
            if not data:
                break
            yield data

    sha256 = hashlib.sha256()
    with open(file_path, "rb") as f:
        for chunk in read_in_chunks(f, 1024 * 1024):  # 1MB
            sha256.update(chunk)
    return sha256.hexdigest()
