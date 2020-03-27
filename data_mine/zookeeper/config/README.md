# Dataset Configuration Files

General information
-------------------

Each dataset has a configuration object inside `config.json`. The configuration
file must be valid when tested against `config_schema.json`.

This [website](https://www.jsonschemavalidator.net/) can be a useful tool during
prototyping and development. It exports a simple interface for schema writing and
real-time validation.


Configuration example (may be outdated)
--------------------------------

```json
[
    {
      "dataset": "RACE",
      "config": {
        "requirements": [
          {
            "URL": "http://www.cs.cmu.edu/~glai1/data/race/RACE.tar.gz",
            "SHA256": "b2769cc9fdc5c546a693300eb9a966cec6870bd349fbc44ed5225f8ad33006e5"
          }
        ]
      }
    }
]
```

Observations
------------

* `expectedFiles` path is relative to the `PROJECT_ROOT` (e.g. the `data_mine/` directory)
and must be a `gzip` compressed file. The paths in the expected files list should be
relative to the dataset directory (e.g. `DATAMINE_DIR/RACE` for `RACE`).
