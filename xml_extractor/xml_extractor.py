import json
from dataclasses import dataclass
from datetime import date
from typing import Dict, List, NoReturn

import pandas as pd
from lxml import etree

from xml_extractor.const import config_path, output_path


@dataclass
class XmlETExtractor:
    main_node: str
    sub_node: str
    key_tag: str
    main_result: pd.DataFrame
    sub_result: pd.DataFrame or None
    """
    this package is used for to learn data extraction from XML file
    """

    @classmethod
    def xml_extractor(cls, xml_template_path: str) -> "XmlETExtractor":
        """
        extract data from xml and store it in class variable
        Args:
            xml_template_path: path of xml file


        Returns: List of Dict

        """
        if XmlETExtractor.is_xml_contents(xml_template_path) is True:
            pass
        temp_main_result = []
        temp_sub_result = []
        config = XmlETExtractor.get_config()
        content = XmlETExtractor.read_xml(xml_template_path)
        if isinstance(content, list):
            for doc in content:
                root = etree.fromstring(doc.encode())
                main_data = XmlETExtractor.get_data(
                    config_data=config[cls.main_node], root=root, target_node=cls.main_node
                )
                temp_main_result.append(main_data)
                if cls.sub_node:
                    sub_data = XmlETExtractor.get_data(
                        config_data=config[cls.sub_node], root=root, target_node=cls.sub_node
                    )
                    try:
                        key_col = main_data[cls.key_tag]
                        main_node_key = cls.main_node.split("/")[-1] + "." + cls.key_tag
                        sub_data[main_node_key] = key_col
                        temp_sub_result.append(sub_data)
                    except ValueError:
                        raise Exception(f"there is no {cls.key_tag} in main node")
        else:
            root = etree.fromstring(content.encode())
            main_data = XmlETExtractor.get_data(config_data=config[cls.main_node], root=root, target_node=cls.main_node)
            temp_main_result.append(main_data)
            if cls.sub_node:
                sub_data = XmlETExtractor.get_data(
                    config_data=config[cls.sub_node], root=root, target_node=cls.sub_node
                )
                try:
                    key_col = main_data[cls.key_tag]
                    main_node_key = cls.main_node.split("/")[-1] + "." + cls.key_tag
                    sub_data[main_node_key] = key_col
                    temp_sub_result.append(sub_data)
                except ValueError:
                    raise Exception(f"there is no {cls.key_tag} in main node")
        cls.main_result = pd.concat(temp_main_result, ignore_index=True)
        if temp_sub_result:
            cls.sub_result = pd.concat(temp_sub_result, ignore_index=True)
            instance = XmlETExtractor(
                main_node=cls.main_node,
                sub_node=cls.sub_node,
                key_tag=cls.key_tag,
                main_result=cls.main_result,
                sub_result=cls.sub_result,
            )
            return instance
        else:
            instance = XmlETExtractor(
                main_node=cls.main_node,
                sub_node=cls.sub_node,
                key_tag=cls.key_tag,
                main_result=cls.main_result,
                sub_result=None,
            )
            return instance

    @staticmethod
    def read_xml(xml_template_path: str) -> str or List[str]:
        """
        read xml file and return it as string
        Args:
            xml_template_path: xml file path

        Returns: xml file as string

        """
        with open(xml_template_path) as file:
            content = file.read()
            if content.count("<?xml") > 1:
                xml_file = content.split("<?xml")[1:]
                for i, doc in enumerate(xml_file):
                    xml_file[i] = "<?xml" + doc
                return xml_file
            else:
                return content

    @staticmethod
    def is_xml_contents(xml_template_path: str) -> bool:
        """
        check if input value is xml file
        Args:
            xml_template_path: xml file path

        Returns: boolean

        """
        if xml_template_path.lower().split(".")[-1] != "xml":
            raise Exception("Error: Wrong file type")
        else:
            return True

    @classmethod
    def get_config(cls) -> Dict:
        """
        get parameter from config.json, used to assign tag to extract
        Returns:Dict template of targeted xml

        """
        with open(config_path) as file:
            config = json.load(file)
            cls.main_node = config["main_node"]
            cls.sub_node = config["sub_node"]
            cls.key_tag = config["key_tag"]
            return config["template"]

    @staticmethod
    def get_data(config_data: dict, root: etree.ElementTree, target_node: str) -> pd.DataFrame or None:
        """
        extract data from xml file
        Args:
            config_data: dict template of xml file
            root: root of xml file
            target_node: tag to extract

        Returns: dataframe of data

        """
        tag = root.findall(target_node)
        if not tag:
            return None
        else:
            pass

        data_list = []

        for child in tag:
            data = {}
            if config_data:
                for key, val in config_data.items():
                    if val == "value":
                        child_key = child.find(key)
                        if child_key is not None:
                            data[key] = child_key.text
                        else:
                            data[key] = None
                    elif val == "attribute":
                        try:
                            data[key] = child.get(key)
                        except ValueError:
                            data[key] = None

            df = pd.DataFrame(data, index=[0])
            data_list.append(df)
        data_list = pd.concat(data_list, ignore_index=True)
        return data_list

    @staticmethod
    def to_parquet(data: pd.DataFrame, node: str) -> NoReturn:
        """
        This method is to format a table of extracted data to parquet
        Args:
            data: targeted data frame
            node: tag that data belong to, used to assign file name

        Returns: No Return

        """
        try:
            main_node_text: str = node.replace("/", "_")
            datetime_suffix: str = date.today().strftime("%Y%m%d")
            data.to_parquet(
                f"{output_path}{main_node_text}_{datetime_suffix}.parquet",
                index=False,
            )
        except OSError:
            raise OSError

    def main_result_to_parquet(self) -> NoReturn:
        """
        callable function to extract convert main data to parquet
        Returns: No Return

        """
        self.to_parquet(self.main_result, self.main_node)

    def sub_result_to_parquet(self) -> NoReturn:
        """
        callable function to extract convert sub data to parquet
        Returns: No Return

        """
        self.to_parquet(self.sub_result, self.sub_node)
