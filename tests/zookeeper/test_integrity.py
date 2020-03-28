import gzip
import os
import unittest

from data_mine import Collection
from data_mine.constants import PROJECT_ROOT
from data_mine.utils import datamine_cache_dir
from data_mine.zookeeper import check_deep_integrity
from data_mine.zookeeper import check_shallow_integrity
from data_mine.zookeeper import load_datasets_config
from pyfakefs.fake_filesystem_unittest import TestCase


class TestDatasetIntegrityCheckFunctions(TestCase):

    # Sets up a fake (in memory) FS with a fake dataset containing
    # the following files:
    #  * file1.txt
    #  * file2.txt
    #  * data/file3.txt
    # The only thing that is not written is the expected files data
    # from the dataset configuration (because this is dependent of
    # the test logic). You can use the available methods exposed in this
    # class (for example: `fake_expected_files_with_wrong_sha256`).
    def setUp(self):
        self.FAKE_DATASET = Collection.RACE
        self.CACHE_DIR = datamine_cache_dir()

        config_dir = os.path.join(PROJECT_ROOT, "zookeeper", "config")

        # Read real (prod) configuration.
        config_str = None
        with open(os.path.join(config_dir, "config.json"), "rt") as f:
            config_str = f.read()

        # Read real (prod) configuraation schema.
        config_schema_str = None
        with open(os.path.join(config_dir, "config_schema.json"), "rt") as f:
            config_schema_str = f.read()

        self.setUpPyfakefs()

        if not os.path.isdir(config_dir):
            os.makedirs(config_dir, mode=0o755)

        # Write the real configuration to the fake FS.
        with open(os.path.join(config_dir, "config.json"), "wt") as g:
            g.write(config_str)
            g.flush()

        # Write the real configuration schema to the fake FS.
        with open(os.path.join(config_dir, "config_schema.json"), "wt") as g:
            g.write(config_schema_str)
            g.flush()

        del config_dir
        del config_str
        del config_schema_str

        # Write the fake files from the dataset:
        #  * file1.txt
        #  * file2.txt
        #  * data/file3.txt
        dataset_dir = os.path.join(self.CACHE_DIR, self.FAKE_DATASET.name)
        if not os.path.isdir(dataset_dir):
            os.makedirs(dataset_dir, mode=0o755)
        to_write = [
                ("file1.txt", "What a beautiful day!"),
                ("file2.txt", "Thank you God!\n"),
                ("data/file3.txt", "Within some inner directory."),
        ]
        for path, contents in to_write:
            path = os.path.join(dataset_dir, path)
            if not os.path.isdir(os.path.dirname(path)):
                os.makedirs(os.path.dirname(path), mode=0o755)
            with open(path, "wt") as g:
                g.write(contents)
                g.flush()

        self.FILE1_SHA = "51a1155af5ffb7bc8daeaca2a6750b065f48ecb0fbaff3daefc014c7a66206c9"  # noqa: E501
        self.FILE2_SHA = "67519f882c41fab92d71c951a1587ba4a46684031f03bc9b2e58c9a9e36c23fb"  # noqa: E501
        self.FILE3_SHA = "55287e7941404e7bfe281f7c2f6dea75685f32329a5682a153229d43f7335532"  # noqa: E501

    def fake_expected_files_with_wrong_sha256(self):
        # Write expected file to the fake FS with bad SHA256 values.
        expected_files_path = load_datasets_config()[self.FAKE_DATASET.name]["expectedFiles"]  # noqa: E501
        expected_files_path = os.path.join(PROJECT_ROOT, expected_files_path)
        dataset_dir = os.path.dirname(os.path.realpath(expected_files_path))
        if not os.path.isdir(dataset_dir):
            os.makedirs(dataset_dir, mode=0o755)

        with gzip.open(expected_files_path, "wb") as g:
            g.write("\n{}  {}\n".format("a" * 64, "file1.txt").encode())
            g.write("{}  {}\n\n\n".format("b" * 64, "file2.txt").encode())
            g.write("{}  {}\n\n".format("c" * 64, "data/file3.txt").encode())

    def fake_expected_files_with_correct_sha256(self):
        # Write expected file to the fake FS with bad SHA256 values.
        expected_files_path = load_datasets_config()[self.FAKE_DATASET.name]["expectedFiles"]  # noqa: E501
        expected_files_path = os.path.join(PROJECT_ROOT, expected_files_path)
        dataset_dir = os.path.dirname(os.path.realpath(expected_files_path))
        if not os.path.isdir(dataset_dir):
            os.makedirs(dataset_dir, mode=0o755)

        with gzip.open(expected_files_path, "wb") as g:
            g.write("{}  {}\n".format(self.FILE1_SHA, "file1.txt").encode())
            g.write("{}  {}\n\n".format(self.FILE2_SHA, "file2.txt").encode())
            g.write("{}  {}".format(self.FILE3_SHA, "data/file3.txt").encode())  # noqa: E501

    def test_shallow_integrity(self):
        self.fake_expected_files_with_correct_sha256()
        self.assertTrue(check_shallow_integrity(self.FAKE_DATASET))

    def test_shallow_integrity_fails_when_file_is_missing(self):
        self.fake_expected_files_with_correct_sha256()
        self.assertTrue(check_shallow_integrity(self.FAKE_DATASET))

        # Remove some file.
        dataset_dir = os.path.join(self.CACHE_DIR, self.FAKE_DATASET.name)
        os.remove(os.path.join(dataset_dir, "file2.txt"))
        self.assertFalse(check_shallow_integrity(self.FAKE_DATASET))

    def test_shallow_integrity_with_extra_files(self):
        self.fake_expected_files_with_correct_sha256()

        # Add a file to the dataset..
        dataset_dir = os.path.join(self.CACHE_DIR, self.FAKE_DATASET.name)
        with open(os.path.join(dataset_dir, "new_file_28.txt"), "wt") as g:
            g.write("Aloha!")
            g.flush()
        self.assertTrue(check_shallow_integrity(self.FAKE_DATASET))

    def test_shallow_integrity_with_wrong_sha(self):
        self.fake_expected_files_with_wrong_sha256()
        self.assertTrue(check_shallow_integrity(self.FAKE_DATASET))

    def test_deep_integrity(self):
        self.fake_expected_files_with_correct_sha256()
        self.assertTrue(check_deep_integrity(self.FAKE_DATASET))

    def test_deep_integrity_with_wrong_sha(self):
        self.fake_expected_files_with_wrong_sha256()
        self.assertFalse(check_deep_integrity(self.FAKE_DATASET))

    def test_deep_integrity_fails_when_file_is_missing(self):
        self.fake_expected_files_with_correct_sha256()
        self.assertTrue(check_deep_integrity(self.FAKE_DATASET))

        # Remove some file.
        dataset_dir = os.path.join(self.CACHE_DIR, self.FAKE_DATASET.name)
        os.remove(os.path.join(dataset_dir, "data/file3.txt"))
        self.assertFalse(check_deep_integrity(self.FAKE_DATASET))

    def test_deep_integrity_with_extra_files(self):
        self.fake_expected_files_with_correct_sha256()

        # Add a file to the dataset..
        dataset_dir = os.path.join(self.CACHE_DIR, self.FAKE_DATASET.name)
        with open(os.path.join(dataset_dir, "new_file_99.txt"), "wt") as g:
            g.write("Aloha!")
            g.flush()
        self.assertTrue(check_deep_integrity(self.FAKE_DATASET))

    def test_integrity_wth_small_file_change(self):
        self.fake_expected_files_with_correct_sha256()
        self.assertTrue(check_deep_integrity(self.FAKE_DATASET))
        self.assertTrue(check_shallow_integrity(self.FAKE_DATASET))

        # Modify a file from the dataset.
        dataset_dir = os.path.join(self.CACHE_DIR, self.FAKE_DATASET.name)
        with open(os.path.join(dataset_dir, "file2.txt"), "at") as g:
            g.write("1")
            g.flush()
        self.assertFalse(check_deep_integrity(self.FAKE_DATASET))
        self.assertTrue(check_shallow_integrity(self.FAKE_DATASET))


if __name__ == '__main__':
    unittest.main()
