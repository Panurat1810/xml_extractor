import os

import pandas as pd

from xml_extractor.xml_extractor import XmlETExtractor

pd.set_option("display.max_columns", None)
pd.set_option("display.expand_frame_repr", False)
pd.set_option("max_colwidth", None)
config_path = os.path.join(os.path.dirname(__file__), "../json_config/sample_book_config.json")
x = XmlETExtractor.xml_extractor("C://Users//PanuratSangchai(Tar)//xml_extractor//sample_book.xml", config_path)
print(x.main_result)
print(x.sub_result)
x.main_result_to_parquet()
