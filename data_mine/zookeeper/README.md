Snapshot a dataset
------------------

```bash
bash snapshot_dataset.sh "dataset_dir" | gzip > expected_files.txt.gz
```

This will automatically generate the `expected_file` contents. The `dataset_dir`
should point to `DATAMINE_CACHE_DIR/DATASET`. Example:

```bash
bash snapshot_dataset.sh ~/.datamine_cache_dir/RACE | gzip > expected_files.txt.gz
```

where:
* `~/.datamine_cache_dir` is the cached directory for all DataMine datasets;
* `RACE` is the name of the dataset (one of `Collection` enum items).
