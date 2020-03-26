

def check_shallow_integrity():
    """
    Verifies if the dataset's local copy is valid in a shallow way.

    The function just checks if the required files are present locally
    and no checksum is checked at all. If you want the checksums
    to be checked, please refer to the `check_deep_integrity` function.

    Returns:
        result (bool): True if the dataset is valid, False otherwise.
    """
    pass


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
