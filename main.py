import glob

from xml_extractor.xml_extractor import XmlETExtractor

x = glob.glob("*.xml")
for path in x:
    data = XmlETExtractor.xml_extractor(path)
    for dataframe in data:
        print(dataframe.head())
