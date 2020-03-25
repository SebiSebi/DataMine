# -*- coding: utf-8 -*-

from __future__ import print_function


def main():
    import sys

    from data_mine.cli import download
    from wasabi import msg

    commands = {
        "download": download,
    }

    if len(sys.argv) <= 1:
        msg.info("Available commands:", ", ".join(commands), exits=1)

    command = sys.argv.pop(1)
    sys.argv[0] = "data_mine {}".format(command)

    if command in commands:
        commands[command]()
    else:
        msg.fail("Unknown command: {}".format(command), exits=1)


if __name__ == "__main__":
    main()
