import pandas as pd

from xml_extractor.xml_extractor import XmlETExtractor

path: str = "data/sample_book.xml"
pd.set_option("display.max_columns", None)
pd.set_option("display.expand_frame_repr", False)
pd.set_option("max_colwidth", None)
x = XmlETExtractor.xml_extractor("C://Users//PanuratSangchai(Tar)//xml_extractor//ipa240229.xml")
x.main_result_to_parquet()
