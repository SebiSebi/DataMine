import json
import os

from data_mine.constants import PROJECT_ROOT
from jsonschema import validate

CONFIG_FILE = os.path.join(PROJECT_ROOT, "zookeeper", "config", "config.json")
CONFIG_SCHEMA_FILE = os.path.join(PROJECT_ROOT, "zookeeper", "config", "config_schema.json")  # noqa: E501


def load_datasets_config():
    """
    Parses the JSON file containing the datasets configuration.

    Moreover, it validates the loaded object against the defined schema.

    Returns:
        config (dict): dictionary of (dataset_id) -> configuration.
    """
    obj = None
    with open(CONFIG_FILE, "rt") as f:
        obj = json.load(f)
    assert(obj is not None)

    schema = None
    with open(CONFIG_SCHEMA_FILE, "rt") as f:
        schema = json.load(f)
    assert(schema is not None)

    # Throws if the object does not obey the schema.
    validate(instance=obj, schema=schema)

    config = {}
    for entry in obj:
        dataset = entry["dataset"] or ""
        assert(dataset not in config)
        config[dataset] = entry["config"]

    return config
