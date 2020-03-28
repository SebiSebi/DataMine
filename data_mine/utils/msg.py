# -*- coding: utf-8 -*-

from __future__ import print_function

import crayons
import inspect
import six
import sys


def maybe_exit(f):
    # Decorator function that checks if `exits` argument is provided.
    # If so, terminates the program with the provided exit code.

    args = None
    if six.PY3:  # pragma: no cover
        args = inspect.getfullargspec(f).args
    else:  # pragma: no cover
        args = inspect.getargspec(f).args  # pylint: disable=deprecated-method
    assert(len(args) == 2)
    assert(args[0] == "message")
    assert(args[1] == "exits")

    def wrapper(*args, **kwargs):
        exit_code = kwargs.get("exits", None)
        if exit_code is None and len(args) >= 2:
            exit_code = args[1]

        ret_value = f(*args, **kwargs)

        if exit_code is not None:
            sys.exit(exit_code)
        return ret_value
    return wrapper

# DO NOT Change the order of the arguments in message functions.
# * `message` must be the first one.
# * `exits` must be the second one.
# We could have used keyword-only arguments but those are only
# available in Python 3 and we don't want to drop Python 2 yet.


def fmt(message, prefix):
    """
    Formats the given message by adding `prefix` at the start of each line.

    If the message is multi-line then split it according to the end-of-line
    terminators and add the prefix string to the start of each line.
    The `prefix` is not added to the beginning of a line if the line is
    completely empty (only whitespace).
    """
    message = str(message).splitlines(True)
    if not message:
        return prefix
    output = ""
    for index, line in enumerate(message):
        if index >= 1 and not line.strip():
            output += line
        else:
            output += "{} {}".format(prefix, line)
    return output


@maybe_exit
def info(message, exits=None):  # pylint: disable=unused-argument
    """
    Displays a message in info style.

    If `exits` is not None, then the program is terminated with the provided
    exit code.
    """
    print(crayons.cyan(fmt(message, "[✓]"), bold=True))
    sys.stdout.flush()


@maybe_exit
def warning(message, exits=None):  # pylint: disable=unused-argument
    """
    Displays a message in info style.

    If `exits` is not None, then the program is terminated with the provided
    exit code.
    """
    print(crayons.yellow(fmt(message, "[!]"), bold=True))
    sys.stdout.flush()


@maybe_exit
def error(message, exits=None):  # pylint: disable=unused-argument
    """
    Displays a message in error style.

    If `exits` is not None, then the program is terminated with the provided
    exit code.
    """
    print(crayons.red(fmt(message, "[✗]"), bold=True))
    sys.stdout.flush()
