import random
import sys
import unittest

from data_mine.zookeeper.download_center import load_config_file
from faker import Faker
if sys.version_info >= (3, 3):
    from unittest.mock import patch, mock_open
else:
    from mock import patch, mock_open


class TestLoadConfigFileFn(unittest.TestCase):

    def setUp(self):
        self.FAKE_FILE = "/my/fake/file/path/with/config"
        self.fake = Faker()

    def generate_good_data(self):
        num_entries = random.randint(30, 50)
        data = []
        for _ in range(0, num_entries):
            data.append((
                self.fake.sha256(raw_output=False),
                random.choice([
                    self.fake.file_path(depth=random.randint(0, 5)),
                    self.fake.file_name()
                ])
            ))
        self.assertEqual(len(data), num_entries)
        return data

    def serialize_ok(self, entries):
        """
        Takes as input an array of pairs (sha, path) and converts to
        a string (file contents) in the expected format: sha256 2-spaces path.
        """
        data = '\n'.join(["{}  {}".format(sha, path) for sha, path in entries])
        return "\n\n" + data + "\n \t\n\n"

    def serialize_bad(self, entries):
        """
        Takes as input an array of pairs (sha, path) and converts to
        a string (file contents) with *a single* space separator.
        """
        return '\n'.join(["{} {}".format(sha, path) for sha, path in entries])

    def test_under_normal_conditions(self):
        entries = self.generate_good_data()
        mock_file = mock_open(read_data=self.serialize_ok(entries))
        with patch('gzip.open', mock_file):
            read_entries = list(load_config_file(self.FAKE_FILE))
            mock_file.assert_called_once_with(self.FAKE_FILE, "rt")
        self.assertEqual(len(entries), len(read_entries))
        for (sha1, path1), (sha2, path2) in zip(entries, read_entries):
            self.assertEqual(sha1, sha2)
            self.assertEqual(path1, path2)

    def test_bad_sha256(self):
        entries = self.generate_good_data()
        entries[1] = ("a" * 31 + " " + ("b" * 32), self.fake.file_name())
        mock_file = mock_open(read_data=self.serialize_ok(entries))
        with patch('gzip.open', mock_file):
            with self.assertRaises(RuntimeError) as context:
                list(load_config_file(self.FAKE_FILE))
            mock_file.assert_called_once_with(self.FAKE_FILE, "rt")
            self.assertIn("Invalid hex SHA256", str(context.exception))

    def test_too_long_sha256(self):
        entries = self.generate_good_data()
        entries[1] = ("a" * 65, self.fake.file_name())
        mock_file = mock_open(read_data=self.serialize_ok(entries))
        with patch('gzip.open', mock_file):
            with self.assertRaises(RuntimeError) as context:
                list(load_config_file(self.FAKE_FILE))
            mock_file.assert_called_once_with(self.FAKE_FILE, "rt")
            self.assertIn("Invalid format", str(context.exception))

    def test_missing_space_separator(self):
        entries = self.generate_good_data()
        mock_file = mock_open(read_data=self.serialize_bad(entries))
        with patch('gzip.open', mock_file):
            with self.assertRaises(RuntimeError) as context:
                list(load_config_file(self.FAKE_FILE))
            mock_file.assert_called_once_with(self.FAKE_FILE, "rt")
            self.assertIn("Invalid format", str(context.exception))


if __name__ == '__main__':
    unittest.main()
