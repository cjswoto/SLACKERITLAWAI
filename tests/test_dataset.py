import os, sys
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))
import json
from pathlib import Path
from slacker_trainer.gui import validate_dataset

def test_validate_dataset_json(tmp_path):
    file = tmp_path / 'data.json'
    json.dump([{"text": "hello"}], open(file, 'w'))
    assert validate_dataset(file)

def test_validate_dataset_invalid(tmp_path):
    file = tmp_path / 'bad.json'
    json.dump([{"nope": "x"}], open(file, 'w'))
    assert not validate_dataset(file)
