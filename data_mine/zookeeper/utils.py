import gzip

SHA256_HEX_LEN = 64  # characters.


def load_integrity_file(file_path):
    """
    Yields tuples of (SHA256_HEX, relative-file-path) from the `file_path`.

    Example:
        * 4140183108 ... f7bef3f0975da9b13510338e37ec5e (64 in total)
        * RACE/data/RACE/train/middle/6645.txt

    The input file path must be in GZIP format with compression 9.
    """
    def parse_line(line):
        if len(line) <= SHA256_HEX_LEN + 2 or line[SHA256_HEX_LEN:SHA256_HEX_LEN + 2] != "  ":  # noqa: E501
            raise RuntimeError(
                "Invalid format for the integrity file. "
                "Expected <sha_256> <2-spaces> <relative_file_path>."
            )
        sha256 = line[:SHA256_HEX_LEN]
        path = line[SHA256_HEX_LEN + 2:].rstrip()
        if not sha256.isalnum():
            raise RuntimeError("Invalid hex SHA256: `{}`".format(sha256))
        return sha256, path

    with gzip.open(file_path, "rb") as f:
        for line in f:
            line = line.decode().strip()
            if len(line) == 0:
                continue
            yield parse_line(line)
