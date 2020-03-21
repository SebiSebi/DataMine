import os


def get_home_dir():
    '''
    Returns the home directory of the current user.

    This is a best guess and may fail to achieve the real objective
    in exotic scenarios.
    '''
    return os.path.expanduser("~")
