import os
from typing import NoReturn

from xml_extractor.xml_extractor import XmlETExtractor

xml_path = os.path.join(os.path.dirname(__file__), "./test_data/test_data.xml")
multiple_xml_path = os.path.join(os.path.dirname(__file__), "./test_data/test_data_multiple.xml")


def test_get_xml_contents_single() -> NoReturn:
    result = XmlETExtractor.get_xml_contents(xml_template_path=xml_path)
    assert isinstance(result, list)
    assert len(result) == 1


def test_get_xml_contents_multiple() -> NoReturn:
    result = XmlETExtractor.get_xml_contents(multiple_xml_path)
    assert isinstance(result, list)
    assert len(result) == 2
