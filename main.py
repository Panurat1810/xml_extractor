from xml_extractor.xml_extractor import XmlETExtractor

path: str = "C://Users//PanuratSangchai(Tar)//xml_extractor//COVID-19 CLinical trials studies//NCT00571389.xml"
x = XmlETExtractor.xml_extractor(path)
counter = 0
for y in x:
    print(y)
    counter += 1
    if counter == 10:
        break
