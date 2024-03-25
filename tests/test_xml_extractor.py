import unittest
from unittest.mock import patch, mock_open
import pandas as pd
from lxml import etree
from io import StringIO

import xml_extractor.xml_extractor

from xml_extractor.xml_extractor import XmlETExtractor

@patch(xml_extractor.xml_extractor.config_path,)
@patch(xml_extractor.xml_extractor.output_path,output_path)

class TestXmlETExtractor(unittest.TestCase):
    def test_read_xml(self, xml_path):
        with open(xml_path) as f:
            content = f.read()
        self.assertEqual(XmlETExtractor.get_xml_contents(xml_path), content)

    def test_is_xml_contents(self, xml_path):
        self.assertTrue(XmlETExtractor.is_xml_content(xml_path))
        with self.assertRaises(Exception):
            XmlETExtractor.is_xml_content("sample.txt")

    def test_get_config(self, config_data):
        config = XmlETExtractor.get_config()
        self.assertEqual(config, config_data["template"])

    def test_get_data(self, config_data, xml_path):
        with open(xml_path) as f:
            content = f.read()
        root = etree.fromstring(content.encode())
        config_data = config_data["template"]
        main_data = XmlETExtractor.get_data(config_data["/root/book"], root, "/root/book")
        expected_main_data = pd.DataFrame(
            [{"id": "1", "title": "Book 1", "price": "10.99"},
             {"id": "2", "title": "Book 2", "price": "12.99"}]
        )
        pd.testing.assert_frame_equal(main_data, expected_main_data)

        sub_data = XmlETExtractor.get_data(config_data["/root/book/author"], root, "/root/book/author")
        expected_sub_data = pd.DataFrame(
            [{"author": "Author 1"}, {"author": "Author 2"}]
        )
        pd.testing.assert_frame_equal(sub_data, expected_sub_data)

    def test_xml_extractor(self, xml_path):
        with open(xml_path) as f:
            content = f.read()
        with patch('builtins.open', mock_open(read_data=content)):
            extractor = XmlETExtractor.xml_extractor(xml_path)
            expected_main_data = pd.DataFrame(
                [{"id": "1", "title": "Book 1", "price": "10.99"},
                 {"id": "2", "title": "Book 2", "price": "12.99"}]
            )
            pd.testing.assert_frame_equal(extractor.main_result, expected_main_data)

            expected_sub_data = pd.DataFrame(
                [{"author": "Author 1", "book.id": "1"},
                 {"author": "Author 2", "book.id": "2"}]
            )
            pd.testing.assert_frame_equal(extractor.sub_result, expected_sub_data)

    def test_to_parquet(self, output_path):
        data = pd.DataFrame({"A": [1, 2, 3]})
        with patch('xml_extractor.output_path', str(output_path)):
            XmlETExtractor.to_parquet(data, "test_node")
        # Check if the file was created
        import os
        expected_file = output_path / f"test_node_{pd.Timestamp.today().strftime('%Y%m%d')}.parquet"
        self.assertTrue(expected_file.exists())

if __name__ == '__main__':
    unittest.main()