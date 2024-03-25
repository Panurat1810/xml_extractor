import pytest
import os
import json


output_path = os.path.join(os.path.dirname(__file__), "test_outputs/")
xml_path = os.path.join(os.path.dirname(__file__), "testdata/sample_book.xml")
config_path = os.path.join(os.path.dirname(__file__), "testjson_config/test_sample_book_config.json")
config_data: dict
with open(config_path) as f:
    config_data = json.load(f)

