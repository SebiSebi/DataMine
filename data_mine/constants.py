"""Various constants used in the project.

Description:

    * DATAMINE_CACHE_DIR_ENV_VAR (str): the name of the environment variable
      whose value dictates where the datasets are downloaded.

    * PROJECT_ROOT (str): the path to the directory containing the main init
      file (the root of the project).
"""
import os


DATAMINE_CACHE_DIR_ENV_VAR = "DATAMINE_CACHE_DIR"
PROJECT_ROOT = os.path.dirname(os.path.abspath(os.path.realpath(__file__)))
