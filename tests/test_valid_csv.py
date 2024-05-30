import pandas as pd
from pathlib import Path
import unittest

REPO = Path(__file__).resolve().parent.parent


def get_corpus_files(
        p: Path = REPO / "data",
        file_name: str = "*.csv"
) -> list[Path]:
    """
    Get and return paths to files matching conditions for the given file_name.

    Args:
        p: the sub-corpus to run.
            Defaults to REPO / "data" (all data files).
        file_name (str): select all files matching this file_name. Defaults to "*.csv"
        using the wildcard "*" to match patterns, in this case all csvs.

    Returns: list of file paths.
    """
    assert p.is_relative_to(REPO)
    assert p.exists()
    return [x for x in p.rglob(file_name)]


class Test(unittest.TestCase):

    def test_all_csvs(self):
        csvs = get_corpus_files()
        for this_csv in csvs:
            print(this_csv)
            pd.read_csv(this_csv)

    def test_meta(self):
        pd.read_csv(REPO / "YCACL_Metadata.csv")