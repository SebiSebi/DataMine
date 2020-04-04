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

There are 2 scripts that can be use to execute tests:
1. `./run_tests.sh` (uses `pytest`). This is usually run by the continuous
integration engine. Not recommended while developing and testing locally.
2. `./green.sh` (uses `green`). This is **recommended** to be used
while developing. It shows friendly messages and summaries.


# Add new dataset

All data files must have `.json` or `.txt.gz` extension to be included
in the PyPI package (please see `setup.py`).
