from ingest.utils import dedupe_example

def test_dedupe_example():
    assert dedupe_example([1,1,2]) == [1,2]
