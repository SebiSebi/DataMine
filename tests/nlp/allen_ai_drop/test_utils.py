import os
import unittest

from data_mine.nlp.allen_ai_drop import DROPType
from data_mine.nlp.allen_ai_drop.utils import serialize_date
from data_mine.nlp.allen_ai_drop.utils import type_to_data_file


class TestUtilFunctions(unittest.TestCase):

    def test_type_to_data_file(self):
        for drop_type in DROPType:
            path = type_to_data_file(drop_type)
            self.assertIn(drop_type.name.lower(), os.path.basename(path))
            self.assertTrue(path.endswith("{}.json".format(drop_type.name.lower())))  # noqa: E501

        self.assertTrue(type_to_data_file(DROPType.TRAIN).endswith("train.json"))  # noqa: E501
        self.assertTrue(type_to_data_file(DROPType.DEV).endswith("dev.json"))  # noqa: E501

    def test_serialize_date(self):
        tests = [
                # ((day, month, year), expected_result)
                (("12", "January", "1995"), "12 January 1995"),
                (("", "January", "1995"), "January 1995"),
                (("12", "", "1996"), "12 1996"),
                (("12", "January", ""), "12 January"),
                (("", "March", ""), "March"),
                (("", "", "2020"), "2020"),
                (("", "", ""), ""),
                ((0, "April", "2002"), "0 April 2002"),
                (("0", "April", 0), "0 April 0"),
                ((0, "June", "0"), "0 June 0"),
                ((25, "February", 2010), "25 February 2010")

        ]
        for (day, month, year), expected_result in tests:
            result = serialize_date({
                "day": day,
                "month": month,
                "year": year
            })
            self.assertEqual(result, expected_result)

        # Missing or None fields.
        self.assertEqual(
                serialize_date({"day": "12", "year": "1850"}),
                "12 1850"
        )
        self.assertEqual(
                serialize_date({"day": "30", "month": "July"}),
                "30 July"
        )
        self.assertEqual(
                serialize_date({"day": None, "month": "September"}),
                "September"
        )

        # Different "order".
        self.assertEqual(
                serialize_date({"year": 1992, "day": 5, "month": "August"}),
                "5 August 1992"
        )
        self.assertEqual(
                serialize_date({"month": "March", "year": 1645, "day": "23"}),
                "23 March 1645"
        )

        # Invalid fields.
        with self.assertRaises(AssertionError):
            serialize_date({"Month": "March"})


if __name__ == '__main__':
    unittest.main()
