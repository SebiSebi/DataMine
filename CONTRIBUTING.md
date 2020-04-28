## Bumping version

We use [bumpversion](https://pypi.org/project/bumpversion/) to make the task
of managing versions easier. `bumpversion` is configured to automatically
modify the desired variables in all the required files: `setup.py`,
`__init__.py`, etc.

There are a couple of steps to be taken for bumping to a new version:
1. Run `bumpversion [part]`, where `part` can one of `major`, `minor` and `patch`
(`{major}.{minor}.{patch}`). The command modifies the necessary files, creates a
new Git tag and commits the changes;
2. Push the new commit (**don't forget the** `--tags` flag): `git push --tags -u origin master`.


# Upload to PyPI

1. Bump to a new version (please refer to the instructions for doing this);
2. Execute: `python setup.py sdist`;
3. Execute: `twine upload dist/data_mine-[new_version].tar.gz` and provide
your credentials.


# Run tests

Use the following command:
* `bash run_tests.sh` (uses `green`). This is **recommended** to be used
while developing. It shows friendly messages and summaries.


# Add new dataset

We are going to demonstrate the steps that need to be followed in order to add
a new dataset to the collection. In this tutorial, we take as an example
the AllenAI's [DROP](https://allennlp.org/drop) dataset.

1. Edit the `Collection` enum inside `data_mine/collection.py` file by adding
a new entry for your dataset. The name you choose for the collection cannot
be changed at a later time. Do not use names that are too common (e.g. "questions",
"qa", "qa_dataset") as they will be reserved essentially for forever. In our case,
`DROP` would be a good name, but a better one is `ALLEN_AI_DROP` (as `DROP` may
interfere with other datasets).

2. Create a directory for your dataset. This should be scoped under the right
category (e.g. if the dataset targets natural language processing, it should be
under `nlp`). In our case, we created `data_mine/nlp/allen_ai_drop`. It must be
a valid Python module (e.g. make sure it contains `__init__.py`). We will refer
to this directory as the dataset directory for the rest of this tutorial.

3. Specify the files that need to be downloaded as part of the dataset. We have
completely automated this process, so you only need to define some URLs. Edit the
configuration file at `data_mine/zookeeper/config/config.json` and add a new
entry for your dataset, containing two things:
    * The requirements, being URLs to download and their SHA256 checksums;
    * The expected files that are part of the dataset. Those can be the files
from the requirements, but this is not always true. After a requirement is
downloaded, if it is an archive, we decompress it and unpack the contents. In this
case, the expected files are the contents of the archive. The expected files config
is also used to check if, for example, a user accidentally modifies a dataset file.
In this case, the checksums would not match and a re-download action will be
automatically triggered. The same thing happens if files are removed.

```json
{
    "dataset": "ALLEN_AI_DROP",
    "config": {
        "requirements": [
            {
                "URL": "https://s3-us-west-2.amazonaws.com/allennlp/datasets/drop/drop_dataset.zip",
                "SHA256": "39d2278a29fd729de301b111a45f434c24834f40df8f4ff116d864589e3249d6"
            }
        ],
        "expectedFiles": "nlp/allen_ai_drop/expected_files.txt.gz"
    }
}
```

4. Edit the config JSON schema `data_mine/zookeeper/config/config_schema.json` and
add your dataset to the array of valid dataset names. Look for the place where
all the datasets are defined in the file, and just append a name to it.

5. It's time we fill in the contents of the expected file. You need to manually
download the required files put all of them in a single directory and extract the
archives (if any). If a requirement is not an archive, leave it as it is. Make sure
to remove all the extracted archives after unpacking, such that only their contents
are part of the dataset. In our case, we created `/tmp/drop/`, downloaded the single
requirement to `/tmp/drop/drop_dataset.zip` then unzipped it. After this process, we
are left with the following directory structure:

```
drop
└── drop_dataset
    ├── drop_dataset_dev.json
    ├── drop_dataset_train.json
    └── license.txt

1 directory, 3 files
```

Notice that the `drop_dataset.zip` archive contained three files:
* `drop_dataset/drop_dataset_dev.json`
* `drop_dataset/drop_dataset_train.json`
* `drop_dataset/license.txt`

Run the script `data_mine/zookeeper/snapshot_dataset.sh` with a single argument:
the path to the directory containing the dataset files. In our case, we executed:
`bash snapshot_dataset.sh /tmp/drop`. It generated the following lines:

```
91ea8537803fce5d9999988c9e83c8d21e0e4feaee09cbfb686470d4d789a10d  drop_dataset/license.txt
6b057fc18cc969e2c548aa6e3b891d1d9ff5930cb3beee90f0e30610fd53724b  drop_dataset/drop_dataset_train.json
f25f09a9e939e946dbb37799b3b3e2c2a9f7416e524017cc4a79780f2ba6edca  drop_dataset/drop_dataset_dev.json
```

Those are the contents of the `nlp/allen_ai_drop/expected_files.txt.gz` (before gzipping them).
Each line is a file from our dataset and the corresponding SHA256. We just need to gzip the
contents (as a side note, some datasets have a huge number of files, that is why we compress
the contents). Full command:

```bash
bash data_mine/zookeeper/snapshot_dataset.sh /tmp/drop | gzip > data_mine/nlp/allen_ai_drop/expected_files.txt.gz
```

**Note:** The expected files configuration must point to a `.txt.gz` file.

6. At this point you can run `python -m data_mine download ALLEN_AI_DROP`. This would
download the dataset to the `DataMine` cache dir (defaults to `~/.datamine_cache_dir`).

7. Create the dataset sub-types by defining an Enum in the file: `data_mine/nlp/allen_ai_drop/types.py`
(you need to create the file). Those are usually train, dev and test sub-datasets. The `DROP`
dataset comes with a train and dev split. The test dataset is hidden. Therefore, we defined
it's sub-types as follows:

```python
from enum import Enum, unique


@unique
class DROPType(Enum):
    TRAIN = 1
    DEV = 2
```

8. Create the loader method at `data_mine/nlp/allen_ai_drop/loader.py`. The method
receives a single argument: the sub-type indicating whether to load the train split
or the dev one. The method has to parse the files and returns a single `Pandas DataFrame`.

```python
from data_mine import Collection
from data_mine.zookeeper import check_shallow_integrity, download_dataset

from .types import DROPType


def DROPDataset(drop_type):
    """
    TODO(sebisebi): add description
    """
    assert(isinstance(drop_type, DROPType))
    download_dataset(Collection.ALLEN_AI_DROP, check_shallow_integrity)
    raise NotImplementedError("TODO: parse and return a DF")
```

You usually want to add this method to the `__init__.py` file of the dataset module:

```python
from .loader import DROPDataset
from .types import DROPType
```

9. Define the main entrypoint method inside `data_mine/__init__.py`:

```python
def ALLEN_AI_DROP(*args, **kwargs):
    from data_mine.nlp.allen_ai_drop import DROPDataset
    return DROPDataset(*args, **kwargs)
```
**Note:** All data files you add should either be a `.json` or a `.txt.gz`. Other extensions
will **not** be included in the PyPI package (please see `setup.py`).

10. Commit and submit a push request. All the code needs to be tested.
This [commit](https://github.com/SebiSebi/DataMine/commit/806825312ab8d225b2519e7611aa532dce1aa968)
encapsulates all steps we described for adding the `ALLEN_AI_DROP` dataset.

