# -*- coding: utf-8 -*-

import hashlib
import os
import requests

from data_mine.utils import file_sha256
from six import string_types
from tqdm import tqdm


def download_file(url, output_file_path, expected_sha256=None):
    """
    Downloads the resource from `url` and saves it to the `output_file_path`.

    No decoding is performed, raw data is retrieved and saved to the disk.

    If the expected SHA256 is provided, the data is checked for
    corruption. If the data is corrupted, a RuntimeError is raised.
    """
    assert(isinstance(url, string_types))
    assert(isinstance(output_file_path, string_types))
    assert(expected_sha256 is None or isinstance(expected_sha256, string_types))  # noqa: E501

    # Iterates through a request data yielding chunks. To be used along
    # with Response.raw (see the comment below).
    def data_iterator(raw_response, chunk_size=1024):
        d = raw_response.read(chunk_size)
        while d:
            yield d
            d = raw_response.read(chunk_size)

    # An important note about using Response.iter_content versus Response.raw.
    # Response.iter_content will automatically decode the gzip and deflate
    # transfer-encodings. Response.raw is a raw stream of bytes – it does not
    # transform the response content. If you really need access to the bytes
    # as they were returned, use Response.raw.
    with requests.get(url, stream=True) as req:
        req.raise_for_status()  # Will raise exception if status != 200.

        total_size = int(req.headers.get('content-length', 0))  # in bytes.
        block_size = 1 * 1024 * 1024

        progress_bar = tqdm(total=total_size, unit='B', unit_scale=True)
        sha256 = hashlib.sha256()
        with open(output_file_path, 'wb') as g:
            for data in data_iterator(req.raw, block_size):
                if not data:  # pragma: no cover
                    continue
                g.write(data)
                sha256.update(data)
                progress_bar.update(len(data))
            g.flush()
        progress_bar.close()

        sha256 = sha256.hexdigest()
        if expected_sha256 is not None and expected_sha256 != sha256:
            raise RuntimeError(
                    "Downloaded file is corrupt. SHA256 = {}".format(sha256)
            )


def download_file_if_missing(url, output_file_path, expected_sha256=None):
    """
    Downloads the resource from `url` and saves it locally only if missing.

    If the file exists and the sha256 sum is correct, then no download is
    performed. Otherwise the file is downloaded from the given URL.
    The sha256 sum will be always verified (if provided). Therefore, if
    this function executes successfully it is guaranteed that we have a
    local copy of the requested file and the local data is not corrupted.

    Note: if `expected_sha256` is not provided (e.g. None) then no integrity
    chech is performed. That is, it only matters if the file is found on the
    local disk (corrupted or not).
    """
    assert(isinstance(url, string_types))
    assert(isinstance(output_file_path, string_types))
    assert(expected_sha256 is None or isinstance(expected_sha256, string_types))  # noqa: E501

    def verify_file_hash():
        if expected_sha256 is None:
            return True
        return file_sha256(output_file_path) == expected_sha256

    if os.path.isfile(output_file_path) and verify_file_hash():
        return  # The file could be found locally.

    # Otherwise, download the data from the provided URL.
    download_file(url, output_file_path, expected_sha256)
