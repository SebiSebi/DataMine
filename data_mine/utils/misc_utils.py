import decimal
import hashlib
import os
import threading

from data_mine.constants import DATAMINE_CACHE_DIR_ENV_VAR
from data_mine.utils import msg
from six import string_types
try:
    from urllib.parse import urlparse
except ImportError:  # pragma: no cover
    from urlparse import urlparse
try:
    from urllib.parse import unquote_plus
except ImportError:  # pragma: no cover
    from urllib import unquote_plus

# Protects the operations in the `datamine_cache_dir` function.
_DATAMINE_CACHE_DIR_LOCK = threading.Lock()


def get_home_dir():
    """
    Returns the home directory of the current user.

    This is a best guess and may fail to achieve the real objective
    in exotic scenarios.
    """
    return os.path.expanduser("~")


def datamine_cache_dir():
    """
    Returns the directory where datasets are stored.

    Preference order:

    1. DATAMINE_CACHE_DIR_ENV_VAR environment variable.
    2. Default directory.

    The operations are not thread safe so we protect everything with
    a lock (module level lock).
    """
    cache_dir = (
            os.getenv(DATAMINE_CACHE_DIR_ENV_VAR, "") or
            os.path.join(get_home_dir(), ".datamine_cache_dir")
    )

    # Normalize the directory path (e.g. expand "..", symlinks, etc.)
    # * expanduser deals with '~' (only it can do that);
    # * realpath deals with symlinks (and possibly relative paths);
    # * abspath deals with relative paths (e.g. ".", "..").
    cache_dir = os.path.abspath(os.path.realpath(os.path.expanduser(cache_dir)))  # noqa: E501

    # Create the directory (including the parents), if missing.
    with _DATAMINE_CACHE_DIR_LOCK:
        if os.path.isfile(cache_dir):
            msg.error("The cached directory `{}` is a file.".format(cache_dir), exits=1)  # noqa: E501
        elif not os.path.isdir(cache_dir):
            os.makedirs(cache_dir, mode=0o755)
    return cache_dir


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


def url_to_filename(url):
    """
    Returns the filename from the URL specification.

    Example: `http://website.com/kyle/dir/img.jpg` -> `img.jpg`.
    It can parse arbitrary (valid) urls including those that contain
    complext query strings and percent encodings.

    If no filename can be found in the URL, the function returns None.
    Example: `http://website.com` -> None
    Example: `http://website.com/dir/` -> None
    """
    path = urlparse(url).path
    if not path:
        return None
    path = unquote_plus(path)  # Deal with percent encoding.
    return os.path.basename(path) or None


def is_integer(number):
    """
    Returns true if and only if the data represented by `number` is an
    integer. The argument can be a string, int or a float object.

    Example: is_integer(2) => True
    Example: is_integer(2.5) => False
    Example: is_integer("10") => True
    Example: is_integer(1.00) => True
    """
    try:
        number = float(number)
        return number.is_integer()
    except ValueError:
        return False


def num_decimal_places(number, safe=True):
    """
    Returns the number of decimans in `number`.

    Note: if number is float, the results may not be what you expect
    because some numbers are not exactly representable in binary floating
    point. For example: 0.1 is 0.100000000000000005551115123... and thus
    num_decimal_places(0.1) would return a large value (about 55"). However,
    if the argument is a string, num_decimal_places("0.1") is exact since
    conversion to float is never happening (it returns 1).

    We recommend that the argument is a string and not a float for exact
    results (see the comment above). If safe is True and the argument is
    a float a ValueError is raised.

    Example: num_decimal_places("0.12") => 2
    Example: num_decimal_places("1.423") => 3
    Example: num_decimal_places("1") => 0
    Example: num_decimal_places(10) => 0
    """
    if safe and isinstance(number, float):
        raise ValueError(
            "Argument is a float and may lead to inexact results due to binary"
            " floating point representation. Safe conversion is not "
            "possible."
        )
    return abs(decimal.Decimal(str(number)).as_tuple().exponent)
