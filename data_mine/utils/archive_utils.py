import os
import patoolib


def is_archive(filepath):
    """
    Checks if the file indicated by `filepath` is a valid arhive.

    An exception is raised if the file does not exist or is not readable.
    This is a best guess checking proceduce and the supported formats
    are those indicated by `patool`: https://github.com/wummel/patool
    """
    assert(os.path.isfile(filepath))
    assert(os.access(filepath, os.R_OK))

    try:
        fmt, compression = patoolib.get_archive_format(filepath)
        patoolib.check_archive_format(fmt, compression)
        program = patoolib.find_archive_program(fmt, 'test')
        patoolib.check_program_compression(filepath, ' test', program, compression)  # noqa: E501
        return True
    except patoolib.util.PatoolError:
        return False


def extract_archive(filepath, outdir):
    """
    Extracts the contents of the archive in the output directory.

    The output directory is required and must be a valid file-system path.
    The output directory and all parent directories are created if missing.
    An exception is raised if the archive does not exist, is not readable
    or is not a valid archive (best guess, not all formats are supported).
    """
    assert(is_archive(filepath))
    patoolib.extract_archive(
            filepath,
            verbosity=-1,
            outdir=outdir,
            interactive=False
    )
