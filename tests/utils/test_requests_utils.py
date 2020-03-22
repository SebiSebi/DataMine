import os
import requests
import responses
import unittest

from data_mine.utils import download_file
from data_mine.utils import download_file_if_missing
from faker import Faker
from tempfile import mkstemp

FAKE_URL = "http://my-fake-url-for-testing/unique"


class TestDownloadFileFn(unittest.TestCase):

    @responses.activate
    def test_small_file(self):
        fake = Faker()
        temp_file_path = None
        temp_fd = None
        try:
            temp_fd, temp_file_path = mkstemp(suffix=fake.pystr(min_chars=10, max_chars=20))  # noqa: E501
            data = fake.pystr(min_chars=10, max_chars=100).encode()
            responses.add(responses.GET, FAKE_URL,
                          body=data, status=200,
                          headers={'content-length': str(len(data))},
                          stream=True)
            download_file(FAKE_URL, temp_file_path)
            with open(temp_file_path, 'rb') as g:
                self.assertEqual(g.read(), data)
        finally:
            if temp_fd:
                os.close(temp_fd)
            if temp_file_path:
                os.remove(temp_file_path)

    @responses.activate
    def test_large_file(self):
        fake = Faker()
        temp_file_path = None
        temp_fd = None
        try:
            temp_fd, temp_file_path = mkstemp(suffix=fake.pystr(min_chars=10, max_chars=20))  # noqa: E501
            data = fake.pystr(min_chars=1024, max_chars=1048).encode() * 10240
            self.assertGreaterEqual(len(data), 10 * 1024 * 1024)
            responses.add(responses.GET, FAKE_URL,
                          body=data, status=200,
                          headers={'content-length': str(len(data))},
                          stream=True)
            download_file(FAKE_URL, temp_file_path)
            with open(temp_file_path, 'rb') as g:
                self.assertEqual(g.read(), data)
        finally:
            if temp_fd:
                os.close(temp_fd)
            if temp_file_path:
                os.remove(temp_file_path)

    @responses.activate
    def test_no_content_length_header(self):
        fake = Faker()
        temp_file_path = None
        temp_fd = None
        try:
            temp_fd, temp_file_path = mkstemp(suffix=fake.pystr(min_chars=10, max_chars=20))  # noqa: E501
            data = fake.pystr(min_chars=50, max_chars=125).encode()
            responses.add(responses.GET, FAKE_URL,
                          body=data, status=200, stream=True)
            download_file(FAKE_URL, temp_file_path)
            with open(temp_file_path, 'rb') as g:
                self.assertEqual(g.read(), data)
        finally:
            if temp_fd:
                os.close(temp_fd)
            if temp_file_path:
                os.remove(temp_file_path)

    @responses.activate
    def test_file_not_found(self):
        responses.add(responses.GET, FAKE_URL,
                      json={'error': 'not found'}, status=404)
        with self.assertRaises(requests.exceptions.HTTPError) as context:
            download_file(FAKE_URL, "test.txt")
        ex = context.exception
        self.assertIn(FAKE_URL, str(ex))
        self.assertEqual(ex.response.status_code, 404)

    @responses.activate
    def test_good_checksum(self):
        fake = Faker()
        temp_file_path = None
        temp_fd = None
        try:
            fake_suffix = fake.pystr(min_chars=10, max_chars=20)
            temp_fd, temp_file_path = mkstemp(suffix=fake_suffix)
            del fake_suffix

            data = "This is a fake file".encode()
            responses.add(responses.GET, FAKE_URL,
                          body=data, status=200,
                          headers={'content-length': str(len(data))},
                          stream=True)
            sha256 = "4d710103e738f5e3c04bbaa549a2ccc3616ca683dab90f068d3bf77517791eab"  # noqa: E501
            download_file(FAKE_URL, temp_file_path, sha256)
            with open(temp_file_path, 'rb') as g:
                self.assertEqual(g.read(), data)
        finally:
            if temp_fd:
                os.close(temp_fd)
            if temp_file_path:
                os.remove(temp_file_path)

    @responses.activate
    def test_wrong_checksum(self):
        fake = Faker()
        temp_file_path = None
        temp_fd = None
        try:
            fake_suffix = fake.pystr(min_chars=10, max_chars=20)
            temp_fd, temp_file_path = mkstemp(suffix=fake_suffix)
            del fake_suffix

            data = "Exception is raised if file is corrupt.".encode()
            responses.add(responses.GET, FAKE_URL,
                          body=data, status=200,
                          headers={'content-length': str(len(data))},
                          stream=True)
            with self.assertRaises(RuntimeError) as context:
                download_file(FAKE_URL, temp_file_path, "sha256")
            ex = context.exception
            self.assertIn("Downloaded file is corrupt", str(ex))
        finally:
            if temp_fd:
                os.close(temp_fd)
            if temp_file_path:
                os.remove(temp_file_path)


class TestDownloadFileIfMissingFn(unittest.TestCase):

    def setUp(self):
        self.file_contents = "Unit testing is awesome!"
        self.correct_sha256 = "8c0c59c1aa6348baa0bea76640da481fcc0a9493f5b484c94bc6ea9f311858f8"  # noqa: E501

    def tearDown(self):
        pass

    def fake_download_response(self):
        data = self.file_contents.encode()
        responses.add(
                responses.GET, FAKE_URL,
                body=data, status=200,
                headers={'content-length': str(len(data))},
                stream=True
        )

    def good_data(self, downloaded_file):
        with open(downloaded_file, "rt") as f:
            return f.read() == self.file_contents

    @responses.activate
    def test_when_file_is_missing(self):
        # A flaky way of generating a temporary file name without the file.
        fake = Faker()
        fake_suffix = fake.pystr(min_chars=15, max_chars=25)
        temp_fd, temp_file_path = mkstemp(suffix=fake_suffix)
        del fake_suffix

        os.close(temp_fd)
        os.remove(temp_file_path)

        self.fake_download_response()

        self.assertFalse(os.path.isfile(temp_file_path))
        download_file_if_missing(FAKE_URL, temp_file_path, self.correct_sha256)
        self.assertTrue(os.path.isfile(temp_file_path))
        self.assertTrue(self.good_data(temp_file_path))
        os.remove(temp_file_path)

    @responses.activate
    def test_when_file_is_corrupt(self):
        fake = Faker()
        fake_suffix = fake.pystr(min_chars=15, max_chars=25)
        temp_fd, temp_file_path = mkstemp(suffix=fake_suffix)
        os.close(temp_fd)
        del fake_suffix

        # Write some modified data to the file.
        with open(temp_file_path, "wb") as g:
            g.write(self.file_contents.encode() * 10)
        self.fake_download_response()

        self.assertTrue(os.path.isfile(temp_file_path))
        download_file_if_missing(FAKE_URL, temp_file_path, self.correct_sha256)
        self.assertTrue(os.path.isfile(temp_file_path))
        self.assertTrue(self.good_data(temp_file_path))
        os.remove(temp_file_path)

    def test_when_file_is_ok(self):
        fake = Faker()
        fake_suffix = fake.pystr(min_chars=10, max_chars=15)
        temp_fd, temp_file_path = mkstemp(suffix=fake_suffix)
        os.close(temp_fd)
        del fake_suffix

        # Write the good contents to the file.
        with open(temp_file_path, "wt") as g:
            g.write(self.file_contents)

        self.assertTrue(os.path.isfile(temp_file_path))
        download_file_if_missing(FAKE_URL, temp_file_path, self.correct_sha256)
        self.assertTrue(os.path.isfile(temp_file_path))
        self.assertTrue(self.good_data(temp_file_path))
        os.remove(temp_file_path)

    def test_when_file_is_corrupt_but_checksum_not_provided(self):
        fake = Faker()
        fake_suffix = fake.pystr(min_chars=15, max_chars=25)
        temp_fd, temp_file_path = mkstemp(suffix=fake_suffix)
        os.close(temp_fd)
        del fake_suffix

        # Write some modified data to the file.
        with open(temp_file_path, "wt") as g:
            g.write(self.file_contents * 5)

        self.assertTrue(os.path.isfile(temp_file_path))
        download_file_if_missing(FAKE_URL, temp_file_path)
        self.assertTrue(os.path.isfile(temp_file_path))
        self.assertFalse(self.good_data(temp_file_path))
        os.remove(temp_file_path)


if __name__ == '__main__':
    unittest.main()
