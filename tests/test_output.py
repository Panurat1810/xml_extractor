import glob
import os
from datetime import date
from typing import NoReturn

from xml_extractor.const import output_path
from xml_extractor.xml_extractor import XmlETExtractor

test_config_path = os.path.join(os.path.dirname(__file__), "test_json_config/test_config.json")
test_xml_path = os.path.join(os.path.dirname(__file__), "./test_data/test_data.xml")


def test_output() -> NoReturn:
    test = XmlETExtractor.xml_extractor(config_path=test_config_path, xml_template_path=test_xml_path)
    test.main_result_to_parquet()
    test.sub_result_to_parquet()

    main_node_text: str = test.main_node.replace("/", "_")
    sub_node_text: str = test.sub_node.replace("/", "_")
    datetime_suffix: str = date.today().strftime("%Y%m%d")
    parquet_file = glob.glob(f"{output_path}*.parquet")

    assert len(parquet_file) > 0
    assert os.path.exists(f"{output_path}{main_node_text}_{datetime_suffix}.parquet")
    assert os.path.exists(f"{output_path}{sub_node_text}_{datetime_suffix}.parquet")

    os.remove(f"{output_path}{main_node_text}_{datetime_suffix}.parquet")
    os.remove(f"{output_path}{sub_node_text}_{datetime_suffix}.parquet")
