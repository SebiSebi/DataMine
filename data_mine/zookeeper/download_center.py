import os

from data_mine import Collection
from data_mine.utils import msg
from data_mine.utils import (
        datamine_cache_dir,
        download_file_if_missing,
        extract_archive,
        is_archive,
        url_to_filename
)
from data_mine.zookeeper.config import load_datasets_config


def download_dataset(dataset_id, integrity_check):
    """
    Downloads a dataset identified by it's dataset ID (Collection).

    The maybe already downloaded local copy is checked for integrity
    according to the specified integrity check. If the local version is up to
    date, then nothing is done. Otherwise, the dataset is downloaded.

    Returns a code (int): with the following semantics:
    * 1: dataset is available locally and the integrity check passed;
    * 2: the dataset has been downloaded (was not available locally).
    """
    assert(isinstance(dataset_id, Collection))
    if integrity_check(dataset_id):  # Dataset is already downloaded.
        return 1
    msg.info("Downloading {} ...".format(dataset_id.name))
    config = load_datasets_config()[dataset_id.name]
    dataset_dir = os.path.join(datamine_cache_dir(), dataset_id.name)
    if not os.path.exists(dataset_dir):
        os.makedirs(dataset_dir, mode=0o755)

    # Download all the requirements.
    for requirement in config["requirements"]:
        url = requirement["URL"]
        expected_sha256 = requirement["SHA256"]

        # Attempt to guess the filename from the URL. In the future,
        # if it is required, we may have another field in the requirements.
        filename = url_to_filename(url)
        assert(filename is not None and len(filename) > 0)
        filepath = os.path.join(dataset_dir, filename)

        download_file_if_missing(
                url, filepath,
                expected_sha256=expected_sha256,
                desc="Downloading {}".format(filename)
        )
        assert(os.path.isfile(filepath))

        # Unpack the file if it is archived or compressed.
        if is_archive(filepath):
            msg.info("Unpacking {} ...".format(filename))
            extract_archive(filepath, outdir=dataset_dir)
    msg.info("{} has been downloaded.".format(dataset_id.name))
    return 2
