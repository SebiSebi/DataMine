import sys
import unittest

from data_mine import Collection
from data_mine.cli import download
try:
    from StringIO import StringIO
except ImportError:
    from io import StringIO
if sys.version_info >= (3, 3):
    from unittest.mock import patch, ANY
else:
    from mock import patch, ANY


class TestDownloadCommand(unittest.TestCase):

    def test_wrong_sys_arguments_provided(self):
        # Too few arguments.
        with patch('sys.argv', []):
            with self.assertRaises(AssertionError):
                download()

        # Wrong first argument.
        with patch('sys.argv', ["%this should not work%"]):
            with self.assertRaises(AssertionError):
                download()

        # Only one argument.
        with patch('sys.argv', ["data_mine download"]):
            with self.assertRaises(SystemExit) as context:
                with patch('sys.stdout', new_callable=StringIO) as mks:
                    download()
        self.assertEqual(context.exception.code, 1)
        self.assertIn("[✗] Usage: ", mks.getvalue())

        # Three arguments provided.
        with patch('sys.argv', ["data_mine download", "2", "3"]):
            with self.assertRaises(SystemExit) as context:
                with patch('sys.stdout', new_callable=StringIO) as mks:
                    download()
        self.assertEqual(context.exception.code, 1)
        self.assertIn("[✗] Usage: ", mks.getvalue())

    def test_invalid_dataset_name(self):
        fake_dataset = "5%!@$!$@!%!@%!#12313fasd"
        with patch('sys.argv', ["data_mine download", fake_dataset]):
            with self.assertRaises(SystemExit) as context:
                with patch('sys.stdout', new_callable=StringIO) as mks:
                    download()
        self.assertEqual(context.exception.code, 1)
        self.assertIn("[✗] Invalid dataset", mks.getvalue())
        self.assertIn(fake_dataset, mks.getvalue())

    @patch("data_mine.cli.download_cmd.download_dataset")
    def test_dataset_locally_available(self, mock_download):
        mock_download.return_value = 1
        with patch('sys.argv', ["data_mine download", "RACE"]):
            with patch('sys.stdout', new_callable=StringIO) as mks:
                download()
        self.assertIn("RACE already available", mks.getvalue())
        mock_download.assert_called_once_with(
                Collection.from_str("RACE"), ANY
        )

    @patch("data_mine.cli.download_cmd.download_dataset")
    def test_dataset_is_downloaded_from_remote(self, mock_download):
        mock_download.return_value = 2
        with patch('sys.argv', ["data_mine download", "RACE"]):
            with patch('sys.stdout', new_callable=StringIO) as mks:
                download()
        self.assertNotIn("already available", mks.getvalue())
        mock_download.assert_called_once_with(
                Collection.from_str("RACE"), ANY
        )


if __name__ == '__main__':
    unittest.main()
