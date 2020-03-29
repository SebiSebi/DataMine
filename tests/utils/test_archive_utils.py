import json
import random
import unittest
import numpy as np

from PIL import Image
from data_mine.utils import is_archive
from faker import Faker
from pyfakefs.fake_filesystem_unittest import TestCase


class TestArchiveUtils(TestCase):

    def setUp(self):
        self.setUpPyfakefs()
        self.fake = Faker()

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


if __name__ == '__main__':
    unittest.main()
