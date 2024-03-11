import unittest
from unittest.mock import mock_open, patch
from xml.etree import ElementTree as etree
from typing import NoReturn

import pandas as pd

from xml_extractor.xml_extractor import XmlETExtractor


class TestXmlETExtractor(unittest.TestCase):
    @patch("builtins.open", new_callable=mock_open, read_data="<xml>...</xml>")
    def test_xml_extractor(self, mock_open) -> NoReturn:
        mock_path = "fake/path/to/xml/file.xml"

        with patch.object(etree, "fromstring") as mock_fromstring:
            mock_fromstring.return_value = etree.Element("root")

            result = XmlETExtractor.xml_extractor(mock_path)

            self.assertIsInstance(result, list)
            self.assertEqual(len(result), 3)
            for df in result:
                self.assertIsInstance(df, pd.DataFrame)

        mock_open.assert_called_once_with(mock_path, "r", encoding="utf-8")
