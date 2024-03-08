from dataclasses import dataclass
from typing import List

import pandas as pd
from lxml import etree


@dataclass
class XmlETExtractor:

    @staticmethod
    def get_root(path: str) -> List[pd.DataFrame]:
        publication_reference = pd.DataFrame()
        application_reference = pd.DataFrame()
        text_data = pd.DataFrame()
        with open(path, "r", encoding="utf-8") as file:
            contents = file.read()
            xml_documents = contents.split('<?xml version="1.0" encoding="UTF-8"?>')

            counter = 0
            for xml_doc in xml_documents:
                if counter >= 1:
                    root = etree.fromstring(xml_doc)
                    temp_key_col = ["pr_doc_num", "ar_doc_num"]
                    temp_key_val = []

                    for doc in root.xpath("us-bibliographic-data-application/publication-reference/document-id"):
                        column = []
                        value = []

                        for child in doc:
                            if child is not None:
                                column.append(child.tag)
                                text = list(child.itertext())
                                value.append(" ".join(text))
                                if child.tag == "doc-number":
                                    text = list(child.itertext())
                                    temp_key_val.append(" ".join(text))
                        if counter == 1:
                            publication_reference = pd.DataFrame(columns=column)
                        publication_reference = pd.concat(
                            [
                                publication_reference,
                                pd.DataFrame([value], columns=column),
                            ],
                            ignore_index=True,
                        )

                    for doc in root.xpath("us-bibliographic-data-application/application-reference/document-id"):
                        column = []
                        value = []

                        for child in doc:
                            if child is not None:
                                column.append(child.tag)
                                text = list(child.itertext())
                                value.append(" ".join(text))
                                if child.tag == "doc-number":
                                    text = list(child.itertext())
                                    temp_key_val.append(" ".join(text))

                        if counter == 1:
                            application_reference = pd.DataFrame(columns=column)

                        application_reference = pd.concat(
                            [
                                application_reference,
                                pd.DataFrame([value], columns=column),
                            ],
                            ignore_index=True,
                        )

                    for doc in root.xpath("abstract"):
                        column = []
                        value = []
                        tag = None
                        for child in doc:
                            if child.text is not None:
                                if tag is child.tag:
                                    text = list(child.itertext())
                                    value.append(" ".join(text))
                                    value = [" ".join(value)]
                                else:
                                    text = list(child.itertext())
                                    column.append(child.tag)
                                    value.append(" ".join(text))
                                tag = child.tag

                        if counter == 1:
                            text_data = pd.DataFrame(columns=column)
                        column.extend(temp_key_col)
                        value.extend(temp_key_val)
                        text_data = pd.concat(
                            [text_data, pd.DataFrame([value], columns=column)],
                            ignore_index=True,
                        )

                counter = counter + 1

        data = [application_reference, publication_reference, text_data]
        return data
