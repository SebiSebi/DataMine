import os
import sys

from data_mine import Collection
from data_mine.utils import datamine_cache_dir, msg
from data_mine.zookeeper import check_deep_integrity
from data_mine.zookeeper import download_dataset


def download():
    assert(len(sys.argv) >= 1)
    assert(sys.argv[0] == "data_mine download")

    if len(sys.argv) != 2:
        msg.error("Usage: python -m data_mine download <dataset_name>", exits=1)  # noqa: E501
    dataset_name = sys.argv[1]
    if dataset_name not in set([x.name for x in Collection]):
        msg.error("Invalid dataset: {}".format(dataset_name))
        msg.info("Available datasets:")
        msg.info("\n".join(sorted([x.name for x in Collection])), exits=1)

    dataset_id = Collection.from_str(dataset_name)
    msg.info("Checking if {} is already downloaded ...".format(dataset_name))
    return_code = download_dataset(dataset_id, check_deep_integrity)
    if return_code == 1:
        msg.info("{} already available at: {}".format(
            dataset_name,
            os.path.join(datamine_cache_dir(), dataset_name))
        )
