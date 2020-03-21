import hashlib
import requests

from tqdm import tqdm


def download_file(url, output_file_path, expected_sha256=None):
    '''
    Downloads the resource from `url` and saves the bytes to the
    output file (no decoding is performed, raw data is saved).

    If the expected SHA256 is provided, the data is checked for
    corruption. If the data is corrupted, a RuntimeError is raised.
    '''
    assert(isinstance(url, str))
    assert(isinstance(output_file_path, str))
    assert(expected_sha256 is None or isinstance(expected_sha256, str))

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
