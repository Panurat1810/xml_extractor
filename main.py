import glob

from xml_extractor.xml_extractor import XmlETExtractor

x = glob.glob("*.xml")
for path in x:
    data = XmlETExtractor.get_root(path)
    for dataframe in data:
        print(dataframe.head())

