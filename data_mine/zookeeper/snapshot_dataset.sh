#!/bin/bash

if [ "$#" -ne 1 ]; then
	echo "Usage: bash list_files.sh <DATAMINE_DIR/DATASET>"
	exit 1
fi

dataset_dir=$1

if [[ "${dataset_dir}" == */ ]]; then
	echo "The directory path should not end with a slash (/)."
	exit 2
fi

# shellcheck disable=SC2044
for path in $(find "${dataset_dir}" -type f -printf '%P\n')
do
	sha256=($(sha256sum "${dataset_dir}"/"${path}"))
	echo "${sha256}  ${path}"
done
