import data_mine as dm
import unittest

from data_mine import Collection


class TestCollection(unittest.TestCase):

    def test_from_str_method(self):
        for dataset_id in Collection:
            self.assertEqual(dataset_id, Collection.from_str(dataset_id.name))
        with self.assertRaises(NotImplementedError) as context:
            Collection.from_str("this-is-a-fake-dataset-5%!@%!%@#!#@")
        self.assertIn("is not part of the collection", str(context.exception))

    def test_all_defined_datasets_have_init_entrypoint(self):
        # For all datasets defined inside the global Collection we need a
        # method inside the data_mine/__init__.py method to load the dataset.
        for ds in Collection:
            self.assertTrue(
                    hasattr(dm, ds.name),
                    "Dataset {} has no entrypoint method defined in "
                    "data_mine/__init__.py. Please add a loader method inside "
                    "the main __init__.py file.".format(ds)
            )
            loader = getattr(dm, ds.name)
            self.assertTrue(
                    callable(loader),
                    "The loader for {} is not callable.".format(ds)
            )


if __name__ == '__main__':
    unittest.main()
