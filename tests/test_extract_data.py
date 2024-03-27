import os
from typing import NoReturn

import pandas as pd

from xml_extractor.xml_extractor import XmlETExtractor

xml_path = os.path.join(os.path.dirname(__file__), "./test_data/test_data.xml")
test_config_path = os.path.join(os.path.dirname(__file__), "test_json_config/test_config.json")


def test_extract_data() -> NoReturn:
    config = XmlETExtractor.get_config(test_config_path)

    with open(xml_path) as file:
        xml_content = file.read()

    main_result, sub_result = XmlETExtractor.extract_data(xml_content, config)
    expected_main_result = pd.DataFrame([{"name": "Item 1", "id": "1"}, {"name": "Item 2", "id": "2"}])
    expected_sub_result = pd.DataFrame([{"test": "True", "item.id": "1"}, {"test": "True", "item.id": "2"}])
    pd.testing.assert_frame_equal(main_result, expected_main_result)
    pd.testing.assert_frame_equal(sub_result, expected_sub_result)
