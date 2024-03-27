import json
import os
from typing import NoReturn

import pandas as pd

from xml_extractor.xml_extractor import XmlETExtractor

test_config_path = os.path.join(os.path.dirname(__file__), "test_json_config/test_config.json")
test_xml_path = os.path.join(os.path.dirname(__file__), "./test_data/test_data.xml")


def test_xml_extractor() -> NoReturn:
    with open(test_config_path, "r") as file:
        expected_config = json.load(file)

    config = XmlETExtractor.get_config(test_config_path)
    content = XmlETExtractor.get_xml_contents(test_xml_path)
    main = []
    sub = []
    for doc in content:
        main_temp, sub_temp = XmlETExtractor.extract_data(config=config, xml_content=doc)
        main.append(main_temp)
        sub.append(sub_temp)
    main = pd.concat(main, ignore_index=True)
    sub = pd.concat(sub, ignore_index=True)

    test = XmlETExtractor.xml_extractor(xml_template_path=test_xml_path, config_path=test_config_path)

    assert test.main_node == expected_config["main_node"]
    assert test.sub_node == expected_config["sub_node"]
    assert test.key_tag == expected_config["key_tag"]
    pd.testing.assert_frame_equal(test.main_result, main)
    pd.testing.assert_frame_equal(test.sub_result, sub)
