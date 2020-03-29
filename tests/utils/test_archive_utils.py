import json
import os
import random
import shutil
import six
import sys
import unittest
import numpy as np

from PIL import Image
from data_mine.utils import extract_archive, is_archive
from faker import Faker
from pyfakefs.fake_filesystem_unittest import TestCase
try:
    from StringIO import StringIO
except ImportError:
    from io import StringIO
if sys.version_info >= (3, 3):
    from unittest.mock import patch
else:
    from mock import patch


class TestArchiveUtils(TestCase):

    def setUp(self):
        self.setUpPyfakefs()
        self.fake = Faker()
        self.OUTDIR = "/extracted/inner/"
        os.makedirs(self.OUTDIR, mode=0o755)

        # We also want to test that nothing is logged to stdout or stderr.
        # Mock the `sys.stdout` and `sys.stderr` buffers to fake outputs
        # so that we can test them.
        stdout_patcher = patch('sys.stdout', new_callable=StringIO)
        stderr_patcher = patch('sys.stderr', new_callable=StringIO)
        self.addCleanup(stdout_patcher.stop)
        self.addCleanup(stderr_patcher.stop)
        self.mock_stdout = stdout_patcher.start()
        self.mock_stderr = stderr_patcher.start()

    def tearDown(self):
        self.assertEqual(self.mock_stdout.getvalue(), "")
        self.assertEqual(self.mock_stderr.getvalue(), "")
        shutil.rmtree(self.OUTDIR)

    def num_extracted_files(self):
        total = 0
        for _, _, files in os.walk(self.OUTDIR):
            total += len(files or [])
        return total

    #####################################################################
    #                          Archive formats                          #
    #####################################################################

    def create_tar(self):  # No compression.
        with open("/arch.tar", "wb") as g:
            g.write(self.fake.tar(num_files=7, compression=None))
            g.flush()

    def create_tar_bzip2(self):
        with open("/arch.tar.bz2", "wb") as g:
            g.write(self.fake.tar(num_files=10, compression="bzip2"))
            g.flush()

    def create_tar_gzip(self):
        with open("/arch.tar.gz", "wb") as g:
            g.write(self.fake.tar(num_files=15, compression="gzip"))
            g.flush()

    def create_zip(self):
        with open("/arch.zip", "wb") as g:
            g.write(self.fake.zip(num_files=21, min_file_size=1024))
            g.flush()

    #####################################################################
    #                         Non-archive formats                       #
    #####################################################################

    def create_csv(self):
        with open("/file.csv", "wt") as g:
            g.write(self.fake.csv(
                header=["name", "address"],
                data_columns=('{{name}}', '{{address}}'),
                num_rows=random.randint(100, 500),
                include_row_ids=False
            ))
            g.flush()

    def create_tsv(self):
        with open("/file.tsv", "wt") as g:
            g.write(self.fake.tsv(
                header=["name", "address"],
                data_columns=('{{name}}', '{{address}}'),
                num_rows=random.randint(125, 350),
                include_row_ids=False
            ))
            g.flush()

    def create_json(self):
        obj = self.fake.pydict(random.randint(10, 1000), False, str, int, bool)
        with open("/file.json", "wt") as g:
            g.write(json.dumps(obj, indent=4, sort_keys=True))
            g.flush()

    def create_png(self):
        imarray = np.random.rand(128, 64, 3) * 255
        im = Image.fromarray(imarray.astype('uint8')).convert('RGBA')
        im.save('/file.png')

    #####################################################################
    #                               Tests                               #
    #####################################################################

    def test_is_archive_when_file_is_missing(self):
        with self.assertRaises(AssertionError):
            is_archive("/some/missing/file")

    def test_is_archive_for_tar(self):
        self.create_tar()
        self.assertTrue(is_archive("/arch.tar"))

    def test_is_archive_for_tar_bzip2(self):
        self.create_tar_bzip2()
        self.assertTrue(is_archive("/arch.tar.bz2"))

    def test_is_archive_for_tar_gzip(self):
        self.create_tar_gzip()
        self.assertTrue(is_archive("/arch.tar.gz"))

    def test_is_archive_for_zip(self):
        self.create_zip()
        self.assertTrue(is_archive("/arch.zip"))

    def test_is_archive_for_csv(self):
        self.create_csv()
        self.assertFalse(is_archive("/file.csv"))

    def test_is_archive_for_tsv(self):
        self.create_tsv()
        self.assertFalse(is_archive("/file.tsv"))

    def test_is_archive_for_json(self):
        self.create_json()
        self.assertFalse(is_archive("/file.json"))

    def test_is_archive_for_png(self):
        self.create_png()
        self.assertFalse(is_archive("/file.png"))

    def test_extract_archive_when_file_is_missing(self):
        with self.assertRaises(AssertionError):
            extract_archive("/some/missing/file/2", "not important")

    def test_extract_invalid_archive(self):
        self.create_json()
        with self.assertRaises(AssertionError):
            extract_archive("/file.json", self.OUTDIR)

    def test_extract_archive_to_missing_output_directory(self):
        self.create_zip()
        self.assertTrue(os.path.isdir(self.OUTDIR))
        shutil.rmtree(self.OUTDIR)
        self.assertFalse(os.path.isdir(self.OUTDIR))
        extract_archive("/arch.zip", self.OUTDIR)
        self.assertTrue(os.path.isdir(self.OUTDIR))

    @unittest.skipIf(six.PY2, "Skipping due to tarfile issue in pyfakefs.")
    def test_extract_archive_for_tar(self):
        self.create_tar()
        extract_archive("/arch.tar", self.OUTDIR)
        self.assertEqual(self.num_extracted_files(), 7)

    @unittest.skipIf(six.PY2, "Skipping due to tarfile issue in pyfakefs.")
    def test_extract_archive_for_tar_bzip2(self):
        self.create_tar_bzip2()
        extract_archive("/arch.tar.bz2", self.OUTDIR)
        self.assertEqual(self.num_extracted_files(), 10)

    def test_extract_archive_for_tar_gzip(self):
        self.create_tar_gzip()
        extract_archive("/arch.tar.gz", self.OUTDIR)
        self.assertEqual(self.num_extracted_files(), 15)

    def test_extract_archive_for_zip(self):
        self.create_zip()
        extract_archive("/arch.zip", self.OUTDIR)
        self.assertEqual(self.num_extracted_files(), 21)


if __name__ == '__main__':
    unittest.main()
