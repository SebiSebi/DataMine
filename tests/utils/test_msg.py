# -*- coding: utf-8 -*-

import random
import sys
import unittest

from data_mine.utils import msg
try:
    from StringIO import StringIO
except ImportError:
    from io import StringIO
if sys.version_info >= (3, 3):
    from unittest.mock import patch
else:
    from mock import patch


class TestMsgFunctions(unittest.TestCase):

    @patch('sys.stdout', new_callable=StringIO)
    def test_program_exists_when_required(self, mock_stdout):
        for fn in [msg.info, msg.warning, msg.error]:
            exit_code = random.randint(1, 127)
            with self.assertRaises(SystemExit) as context:
                fn("fake msg 1", exits=exit_code)
            self.assertEqual(context.exception.code, exit_code)

            exit_code = random.randint(1, 127)
            with self.assertRaises(SystemExit) as context:
                fn("fake msg 2", exit_code)
            self.assertEqual(context.exception.code, exit_code)

            fn("another test")  # Should not exit.

        output = mock_stdout.getvalue()
        self.assertIn("fake msg 1\n", output)
        self.assertIn("fake msg 2\n", output)
        self.assertIn("another test\n", output)

    @patch('sys.stdout', new_callable=StringIO)
    def test_info(self, mock_stdout):
        msg.info("info message")
        self.assertEqual(mock_stdout.getvalue(), "[✓] info message\n")

    @patch('sys.stdout', new_callable=StringIO)
    def test_warning(self, mock_stdout):
        msg.warning("warning message")
        self.assertEqual(mock_stdout.getvalue(), "[!] warning message\n")

    @patch('sys.stdout', new_callable=StringIO)
    def test_error(self, mock_stdout):
        msg.error("error message")
        self.assertEqual(mock_stdout.getvalue(), "[✗] error message\n")

    def test_formatting_function(self):
        self.assertEqual(msg.fmt("sebi", "⛄"), "⛄ sebi")
        self.assertEqual(msg.fmt("sebi\n", "⛄"), "⛄ sebi\n")
        self.assertEqual(msg.fmt("sebi\n\n", "⛄"), "⛄ sebi\n\n")
        self.assertEqual(msg.fmt("sebi\ntest", "⛄"), "⛄ sebi\n⛄ test")
        self.assertEqual(msg.fmt("sebi\ntest\n", "⛄"), "⛄ sebi\n⛄ test\n")
        self.assertEqual(msg.fmt("sebi\ntest\n\n\n", "⛄"), "⛄ sebi\n⛄ test\n\n\n")  # noqa: E501
        self.assertEqual(msg.fmt("sebi\\ntest", "⛄"), "⛄ sebi\\ntest")
        self.assertEqual(msg.fmt([1, 2, 3], "⛄"), "⛄ [1, 2, 3]")
        self.assertEqual(msg.fmt("sebi\n ", "⛄"), "⛄ sebi\n ")
        self.assertEqual(msg.fmt("", "⛄"), "⛄")
        self.assertEqual(msg.fmt(" ", "⛄"), "⛄  ")
        self.assertEqual(msg.fmt(" \n", "⛄"), "⛄  \n")
        self.assertEqual(msg.fmt(" \n", "⛄"), "⛄  \n")
        self.assertEqual(msg.fmt(" \ngood", "⛄"), "⛄  \n⛄ good")


if __name__ == '__main__':
    unittest.main()
