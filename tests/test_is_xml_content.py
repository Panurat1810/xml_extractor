from typing import NoReturn

import pytest

from xml_extractor.xml_extractor import XmlETExtractor


def test_is_xml_content_valid() -> NoReturn:
    xml_path = "path/to/file.xml"
    assert XmlETExtractor.is_xml_content(xml_path) is True


def test_is_xml_content_invalid() -> NoReturn:
    non_xml_path = "path/to/file.txt"
    with pytest.raises(Exception, match="Error: Wrong file type"):
        XmlETExtractor.is_xml_content(non_xml_path)
