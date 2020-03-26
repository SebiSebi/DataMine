import jsonschema
import os
import six
import sys
import unittest

from data_mine import Collection
from data_mine.constants import PROJECT_ROOT
from data_mine.zookeeper import load_datasets_config
if sys.version_info >= (3, 3):
    from unittest.mock import mock_open, patch
else:
    from mock import mock_open, patch


class TestDatasetsConfiguration(unittest.TestCase):

    def setUp(self):
        self.collection = set([d.name for d in Collection])
        self.assertIsInstance(self.collection, set)

        if six.PY3:
            self.OPEN_METHOD = "builtins.open"
        else:
            self.OPEN_METHOD = "__builtin__.open"

    def test_prod_config_is_valid(self):
        config = load_datasets_config()
        for dataset in config:
            self.assertIn(dataset, self.collection)

    def test_all_prod_datasets_are_configured(self):
        config = load_datasets_config().keys()
        for dataset in self.collection:
            self.assertIn(dataset, config)

    def test_wrong_config_raises_error(self):
        bad_config = '''
            [
                {
                    "dataset": "RACE",
                    "config": {
                        "requirements": [
                            {
                                "URL": "http://fake-url",
                                "SHA256": "this is not a valid hex SHA256"
                            }
                        ]
                    }
                }
            ]
        '''

        # Load the good schema (kind of a hack) to return in the mock call.
        from data_mine.zookeeper.config.ops import CONFIG_SCHEMA_FILE
        schema = None
        with open(CONFIG_SCHEMA_FILE, "rt") as f:
            schema = f.read()
        self.assertIsNotNone(schema)

        # We are creating two different mock files.
        mk = mk1 = mock_open(read_data=bad_config)
        mk2 = mock_open(read_data=schema)
        mk.side_effect = [mk1.return_value, mk2.return_value]
        with patch(self.OPEN_METHOD, mk):
            with self.assertRaises(jsonschema.exceptions.ValidationError):
                load_datasets_config()
            mk.assert_any_call(os.path.join(PROJECT_ROOT, "zookeeper", "config", "config.json"), "rt"),  # noqa: E501
            mk.assert_any_call(os.path.join(PROJECT_ROOT, "zookeeper", "config", "config_schema.json"), "rt")  # noqa: E501
            self.assertEqual(mk.call_count, 2)


if __name__ == '__main__':
    unittest.main()
