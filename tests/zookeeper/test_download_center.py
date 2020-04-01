import hashlib
import io
import json
import os
import responses
import sys
import unittest
import zipfile

from data_mine import Collection
from data_mine.utils import datamine_cache_dir
from data_mine.zookeeper import download_dataset
from pyfakefs.fake_filesystem_unittest import TestCase
if sys.version_info >= (3, 3):
    from unittest.mock import patch
else:
    from mock import patch


class TestDownloadDatasetFn(TestCase):

    def setUp(self):
        self.setUpPyfakefs()
        self.FAKE_DATASET = Collection.RACE
        self.FAKE_URL_DATA1 = self.fake_url_data()
        self.FAKE_URL_DATA2 = b"This is a JSON file."
        self.FAKE_CONFIG = {
            self.FAKE_DATASET.name: json.loads("""{{
                "requirements": [
                    {{
                        "URL": "http://fake-website.com/my/files.zip",
                        "SHA256": "{0}"
                    }},
                    {{
                        "URL": "http://fake-website.com/my2/file.json",
                        "SHA256": "{1}"
                    }}
                ]
            }}""".format(
                self.bytes_sha256(self.FAKE_URL_DATA1),
                self.bytes_sha256(self.FAKE_URL_DATA2)
            ))
        }  # We use double braces so as to force `format` ignore them.

    # Returns a bytestream with the contents of the fake URL (zip archive).
    def fake_url_data(self):
        all_files = [
                ("1.txt", io.BytesIO(b"First question")),
                ("2.txt", io.BytesIO(b"Second question")),
                ("dir/3.txt", io.BytesIO(b"Third question"))
        ]
        zip_buffer = io.BytesIO()
        with zipfile.ZipFile(zip_buffer, "a") as zip_file:
            for file_name, data in all_files:
                zip_file.writestr(file_name, data.getvalue())
        return zip_buffer.getvalue()

    # Computes the SHA256 of a bytestream and returns the value in hex.
    def bytes_sha256(self, bytestream):
        sha256 = hashlib.sha256()
        sha256.update(bytestream)
        return sha256.hexdigest()

    @patch('data_mine.zookeeper.download_center.load_datasets_config')
    def test_dataset_not_downloaded_if_locally_available(self, mock_fn):
        def fake_integrity_check(dataset_id):
            self.assertEqual(dataset_id, Collection.RACE)
            return True

        return_code = download_dataset(Collection.RACE, fake_integrity_check)
        mock_fn.assert_not_called()
        self.assertEqual(return_code, 1)

    @responses.activate
    @patch('data_mine.zookeeper.download_center.load_datasets_config')
    def test_dataset_is_downloaded_if_missing(self, mock_config):
        mock_config.return_value = self.FAKE_CONFIG
        responses.add(responses.GET, "http://fake-website.com/my/files.zip",
                      body=self.FAKE_URL_DATA1, status=200,
                      headers={'content-length': str(len(self.FAKE_URL_DATA1))},  # noqa: E501
                      stream=True)
        responses.add(responses.GET, "http://fake-website.com/my2/file.json",
                      body=self.FAKE_URL_DATA2, status=200,
                      headers={'content-length': str(len(self.FAKE_URL_DATA2))},  # noqa: E501
                      stream=True)
        return_code = download_dataset(Collection.RACE, lambda _: False)
        self.assertEqual(return_code, 2)

        data_dir = os.path.join(datamine_cache_dir(), self.FAKE_DATASET.name)
        self.assertEqual(
                open(os.path.join(data_dir, "1.txt"), "rt").read(),
                "First question"
        )
        self.assertEqual(
                open(os.path.join(data_dir, "2.txt"), "rt").read(),
                "Second question"
        )
        self.assertEqual(
                open(os.path.join(data_dir, "dir/3.txt"), "rt").read(),
                "Third question"
        )
        self.assertEqual(
                open(os.path.join(data_dir, "file.json"), "rt").read(),
                "This is a JSON file."
        )

    @responses.activate
    @patch('data_mine.zookeeper.download_center.load_datasets_config')
    def test_exception_raised_if_url_not_reachable(self, mock_config):
        # We also check that the dataset directory is not created if existing.
        os.makedirs(
                os.path.join(datamine_cache_dir(), self.FAKE_DATASET.name),
                mode=0o755
        )
        mock_config.return_value = self.FAKE_CONFIG
        with self.assertRaises(Exception):
            download_dataset(Collection.RACE, lambda _: False)


if __name__ == '__main__':
    unittest.main()
