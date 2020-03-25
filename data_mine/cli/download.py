import sys

from data_mine.utils import msg


def download():
    assert(len(sys.argv) >= 1)
    assert(sys.argv[0] == "data_mine download")

    if len(sys.argv) != 2:
        msg.error("Usage: python -m data_mine download <dataset_name>", exit=1)
    dataset_name = sys.argv[1]

    # We perform a deep check of the local copy before downloading.
    msg.info("Downloading {} ...".format(dataset_name))
