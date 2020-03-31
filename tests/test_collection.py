import unittest

from data_mine import Collection


class TestCollection(unittest.TestCase):

    def test_from_str_method(self):
        for dataset_id in Collection:
            self.assertEqual(dataset_id, Collection.from_str(dataset_id.name))
        with self.assertRaises(NotImplementedError) as context:
            Collection.from_str("this-is-a-fake-dataset-5%!@%!%@#!#@")
        self.assertIn("is not part of the collection", str(context.exception))


if __name__ == '__main__':
    unittest.main()
