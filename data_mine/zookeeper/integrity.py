import os

from data_mine import Collection
from data_mine.constants import PROJECT_ROOT
from data_mine.utils import datamine_cache_dir
from data_mine.zookeeper import load_datasets_config
from data_mine.zookeeper.download_center import load_config_file


def check_shallow_integrity(dataset_id):
    """
    Verifies if the dataset's local copy is valid in a shallow way.

    The function just checks if the required files are present locally
    and no checksum is checked at all. If you want the checksums
    to be checked, please refer to the `check_deep_integrity` function.

    Returns:
        result (bool): True if the dataset is valid, False otherwise.
    """
    assert(isinstance(dataset_id, Collection))
    config = load_datasets_config()[dataset_id.name]
    cache_dir = os.path.join(datamine_cache_dir(), dataset_id.name)
    for _, expected_file in load_config_file(os.path.join(PROJECT_ROOT, config["expectedFiles"])):  # noqa: E501
        expected_file = os.path.join(cache_dir, expected_file)
        if not os.path.isfile(expected_file):
            return False
    return True


def check_deep_integrity():
    """
    Verifies if the dataset's local copy is valid in a deep way.

    The function checks if the required files are present locally AND the
    checksums are valid. This function can read a large amount of data from
    the disk (to compute file hashes) and it can be slow. If you want
    a more shallow of integrity verification please refer to the alternative
    function: `check_deep_integrity`.

    Returns:
        result (bool): True if the dataset is valid, False otherwise.
    """
    pass


if __name__ == "__main__":
    print(check_shallow_integrity(Collection.RACE))
