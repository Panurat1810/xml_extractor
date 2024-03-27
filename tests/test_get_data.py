import os
from typing import NoReturn

import pandas as pd
from lxml import etree

from xml_extractor.xml_extractor import XmlETExtractor

xml_path = os.path.join(os.path.dirname(__file__), "./test_data/test_data.xml")
test_config_path = os.path.join(os.path.dirname(__file__), "test_json_config/test_config.json")


def test_get_data() -> NoReturn:
    config = XmlETExtractor.get_config(test_config_path)
    with open(xml_path) as file:
        xml_content = file.read()

    root = etree.fromstring(xml_content.encode())
    target_node = "item"
    result = XmlETExtractor.get_data(config[target_node], root, target_node)

    expected_result = pd.DataFrame([{"name": "Item 1", "id": "1"}, {"name": "Item 2", "id": "2"}])

    pd.testing.assert_frame_equal(result, expected_result)
