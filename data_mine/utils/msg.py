# -*- coding: utf-8 -*-

from __future__ import print_function

import crayons
import sys


def maybe_exit(f):
    # Decorator function that checks if `exit` argument is provided.
    # If so, terminates the program with the provided exit code.
    def wrapper(*args, **kwargs):
        exit = kwargs.get("exit", None)
        if exit is None and len(args) >= 2:
            exit = args[1]

        ret_value = f(*args, **kwargs)

        if exit is not None:
            sys.exit(exit)
        return ret_value
    return wrapper

# DO NOT Change the order of the arguments in message functions.
# * `message` must be the first one.
# * `exit` must be the second one.
# We could have used keyword-only arguments but those are only
# available in Python 3 and we don't want to drop Python 2 yet.


def fmt(message, prefix):
    """
    If the message is multiline then split and add the prefix
    string to each line.
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
def info(message, exit=None):
    """
    Displays a message in info style. If `exit` is not None, then
    the program is terminated with the provided exit code.
    """
    print(crayons.cyan(fmt(message, "[✓]"), bold=True))
    sys.stdout.flush()


@maybe_exit
def error(message, exit=None):
    """
    Displays a message in error style. If `exit` is not None, then
    the program is terminated with the provided exit code.
    """
    print(crayons.red(fmt(message, "[✗]"), bold=True))
    sys.stdout.flush()
