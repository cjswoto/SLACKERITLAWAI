import os
import sys

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from ingest.utils import dedupe_example

def test_dedupe_example():
    assert dedupe_example([1,1,2]) == [1,2]
