import json
from dataclasses import dataclass
from typing import Dict, List, Tuple, Union
import pandas as pd
from lxml import etree
import os
from xml_extractor.config import xml_template_path, main_node, sub_node, key_tag


@dataclass
class XmlETExtractor:
    """
    this package is used for to learn data extraction from XML file
    """

    @staticmethod
    def xml_extractor() -> 'XmlETExtractor':
        """
        extract data from xml in list of data frame
        Args:


        Returns: List of Dict

        """

        if xml_template_path.lower().split(".")[-1] != "xml":
            raise Exception("Error: Wrong file type")
        else:
            pass
        main_result = []
        sub_result = []
        config = XmlETExtractor.config()
        with open(xml_template_path) as file:
            content = file.read()
            if content.count('<?xml') > 1:
                xml_file = content.split('<?xml')[1:]
                for doc in xml_file:
                    root = etree.fromstring(b'<?xml' + doc.encode())
                    main_data = XmlETExtractor.get_data(config_data=config[main_node],
                                                        root=root,
                                                        target_node=main_node)
                    main_result.append(main_data)
                    if sub_node:
                        sub_data = XmlETExtractor.get_data(config_data=config[sub_node],
                                                           root=root,
                                                           target_node=main_node)
                        try:
                            key_col = main_data[key_tag]
                            main_node_key = main_node.split('/')[-1] + '.' + key_tag
                            sub_data[main_node_key] = key_col
                            sub_result.append(sub_data)
                        except ValueError:
                            raise Exception(f"there is no {key_tag} in main node")
            else:
                root = etree.fromstring(content.encode())
                main_data = XmlETExtractor.get_data(config_data=config[main_node],
                                                    root=root,
                                                    target_node=main_node)
                main_result.append(main_data)
                if sub_node:
                    sub_data = XmlETExtractor.get_data(config_data=config[sub_node],
                                                       root=root,
                                                       target_node=main_node)
                    try:
                        key_col = main_data[key_tag]
                        main_node_key = main_node.split('/')[-1] + '.' + key_tag
                        sub_data[main_node_key] = key_col
                        sub_result.append(sub_data)
                    except ValueError:
                        raise Exception(f"there is no {key_tag} in main node")
        main_result = pd.concat(main_result, ignore_index=True)
        if sub_result:
            sub_result = pd.concat(sub_result, ignore_index=True)

        def get_all():
            return main_result, sub_result

        def get_main():
            return main_result

        def get_sub():
            return sub_result

        instance = XmlETExtractor()
        instance.get_all = get_all
        instance.get_main = get_main
        instance.get_sub = get_sub
        instance.main_result = main_result
        instance.sub_result = sub_result if sub_result is not None else None

        return instance

    @staticmethod
    def config() -> Dict or Tuple:
        with open(os.path.join(os.path.dirname(__file__), "config.json")) as file:
            config = json.load(file)['sample_book']
            return config

    @staticmethod
    def get_data(config_data, root, target_node) -> pd.DataFrame:
        root = root.findall(target_node)
        data_list = []

        for child in root:
            data = {}
            if config_data:
                for key, val in config_data.items():
                    elem = child.find(key)
                    if elem is not None:
                        data[key] = elem.text
                    else:
                        try:
                            data[key] = child.get(key)
                        except ValueError:
                            data[key] = None

            df = pd.DataFrame(data, index=[0])
            data_list.append(df)

        data_list = pd.concat(data_list, ignore_index=True)
        return data_list
