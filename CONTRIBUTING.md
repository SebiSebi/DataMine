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
