import gzip
import os
import random
import unittest

from data_mine.zookeeper.utils import load_integrity_file
from faker import Faker
from tempfile import mkstemp


class TestLoadIntegrityFileFn(unittest.TestCase):

    def setUp(self):
        self.fake = Faker()

        # Create the temporary file without any contents.
        fake_suffix = self.fake.pystr(min_chars=15, max_chars=25)
        self.temp_fd, self.temp_file_path = mkstemp(suffix=fake_suffix)
        del fake_suffix

    def tearDown(self):
        os.close(self.temp_fd)
        os.remove(self.temp_file_path)

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

    def write_to_file(self, data):
        with gzip.open(self.temp_file_path, 'wb') as g:
            g.write(data.encode())
            g.flush()

    def read_from_file(self):
        return list(load_integrity_file(self.temp_file_path))

    def test_under_normal_conditions(self):
        entries = self.generate_good_data()
        self.write_to_file(self.serialize_ok(entries))
        self.assertListEqual(self.read_from_file(), entries)

    def test_bad_sha256(self):
        entries = self.generate_good_data()
        entries[1] = ("a" * 31 + " " + ("b" * 32), self.fake.file_name())
        self.write_to_file(self.serialize_ok(entries))
        with self.assertRaises(RuntimeError) as context:
            self.read_from_file()
        self.assertIn("Invalid hex SHA256", str(context.exception))

    def test_too_long_sha256(self):
        entries = self.generate_good_data()
        entries[1] = ("a" * 65, self.fake.file_name())
        self.write_to_file(self.serialize_ok(entries))
        with self.assertRaises(RuntimeError) as context:
            self.read_from_file()
        self.assertIn("Invalid format", str(context.exception))

    def test_missing_space_separator(self):
        entries = self.generate_good_data()
        self.write_to_file(self.serialize_bad(entries))
        with self.assertRaises(RuntimeError) as context:
            self.read_from_file()
        self.assertIn("Invalid format", str(context.exception))


if __name__ == '__main__':
    unittest.main()
