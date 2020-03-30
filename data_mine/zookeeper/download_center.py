from data_mine import Collection


def download_dataset(dataset_id, integrity_check):
    """
    Downloads a dataset identified by it's dataset ID (Collection).

    The maybe already downloaded local copy is checked for integrity
    according to the specified integrity check. If the local version is up to
    date, then nothing is done. Otherwise, the dataset is downloaded.
    """
    assert(isinstance(dataset_id, Collection))
    if integrity_check(dataset_id):  # Dataset is already downloaded.
        return
    print(dataset_id)
