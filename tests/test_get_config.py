import json
import os
from typing import NoReturn

from xml_extractor.xml_extractor import XmlETExtractor

test_config_path = os.path.join(os.path.dirname(__file__), "test_json_config/test_config.json")


def test_get_config() -> NoReturn:
    config = XmlETExtractor.get_config(test_config_path)

    with open(test_config_path, "r") as file:
        expected_config = json.load(file)

    assert config == expected_config["template"]
    assert XmlETExtractor.main_node == expected_config["main_node"]
    assert XmlETExtractor.sub_node == expected_config["sub_node"]
    assert XmlETExtractor.key_tag == expected_config["key_tag"]
