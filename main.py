from xml_extractor.xml_extractor import XmlETExtractor
import pandas as pd

path: str = "/xml_extractor/sample_book.xml"
pd.set_option('display.max_columns', None)
pd.set_option('display.expand_frame_repr', False)
pd.set_option('max_colwidth', None)
x = XmlETExtractor.xml_extractor()

y = x.get_main()
print(y)