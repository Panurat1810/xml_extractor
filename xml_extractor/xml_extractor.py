from dataclasses import dataclass
from typing import Dict, List

import lxml.etree
from lxml import etree


@dataclass
class XmlETExtractor:
    """
    this package is used for to learn data extraction from XML file
    """

    @staticmethod
    def xml_extractor(xml_template_path: str) -> List:
        """
        extract data from xml in list of data frame
        Args:
            xml_template_path: xml file path

        Returns: List of Dict

        """
        if xml_template_path.lower().split(".")[-1] != "xml":
            raise Exception("Error: Wrong file type")
        else:
            pass

        with open(xml_template_path, "r", encoding="utf-8") as file:
            contents = file.read()
            xml_documents = contents.split('<?xml version="1.0" encoding="UTF-8"?>')
            data = []
            counter = 0
            for xml_doc in xml_documents:
                temp_data = []
                if counter >= 1:
                    root = etree.fromstring(xml_doc)
                    x = XmlETExtractor.extract_xml_structure(root)
                    temp_data.append(x)
                counter += 1
                print(counter)
                data.append(temp_data)

        return data

    @staticmethod
    def xml_to_dict(elem: lxml.etree.ElementTree()) -> Dict:
        """
        extract data in dict format
        Args:
            elem:element of xml, get from extract_xml_structure function

        Returns: dict of data

        """
        if len(elem) == 0:
            return elem.text.strip() if elem.text else None
        else:
            result = {}
            for child in elem:
                result[child.tag] = XmlETExtractor.xml_to_dict(child)
            return result

    @staticmethod
    def extract_xml_structure(root: lxml.etree.ElementTree()) -> Dict:
        """
        function for asserting xml structure, if child element has grandchild or not, then send to xml_to_dict accordingly
        Args:
            root: root element of xml

        Returns: Dict of data

        """
        result = {}
        for child in root:
            if len(child) == 0:
                # If the child has no further nested elements, store its text content
                result[child.tag] = XmlETExtractor.xml_to_dict(child)
            else:
                if child.tag in result:
                    if not isinstance(result[child.tag], list):
                        result[child.tag] = [result[child.tag]]
                    result[child.tag].append(XmlETExtractor.xml_to_dict(child))
                else:
                    result[child.tag] = XmlETExtractor.xml_to_dict(child)
        return result
