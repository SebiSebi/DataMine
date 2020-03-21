import os
import requests
import responses
import unittest

from data_mine.utils import download_file
from faker import Faker
from tempfile import mkstemp

FAKE_URL = "http://my-fake-url-for-testing/unique"


class TestDownloadFileUtil(unittest.TestCase):

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


if __name__ == '__main__':
    unittest.main()
