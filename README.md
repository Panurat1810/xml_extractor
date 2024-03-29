### XML Extractor
This package is solely use as a practice of XML data extraction.
package used: [pandas](https://pandas.pydata.org/docs/index.html) [lxml](https://lxml.de/)

### Set up
This package required a json file that contains a template of targeted data, from now on I will call in config.json
I will use sample_book, which is a open source data from [kaggle](https://www.kaggle.com/datasets/zygmunt/goodbooks-10k?select=sample_book.xml)
This is what data looks like:
```dtd
<?xml version="1.0" encoding="UTF-8"?>
<GoodreadsResponse>
  <Request>
    <authentication>true</authentication>
      <key><![CDATA[all_men_must_die]]></key>
    <method><![CDATA[book_show]]></method>
  </Request>
  <book>
  <id>205330</id>
  <title><![CDATA[There Was an Old Lady Who Swallowed a Fly]]></title>
  <isbn><![CDATA[0670869392]]></isbn>
  <isbn13><![CDATA[9780670869398]]></isbn13>
  <asin><![CDATA[]]></asin>
  <kindle_asin><![CDATA[]]></kindle_asin>
  <marketplace_id><![CDATA[]]></marketplace_id>
  <country_code><![CDATA[GB]]></country_code>
  <image_url>https://images.gr-assets.com/books/1172674507m/205330.jpg</image_url>
  <small_image_url>https://images.gr-assets.com/books/1172674507s/205330.jpg</small_image_url>
  <publication_year></publication_year>
  <publication_month></publication_month>
  <publication_day></publication_day>
  <publisher></publisher>
  <language_code></language_code>
  <is_ebook>false</is_ebook>
  <description></description>
```
and this is what config.json look like:
```json
{
  "main_node": "book/similar_books/book",
  "sub_node": "book/similar_books/book/authors/author",
  "key_tag": "id",
  "template": {
    "book": {
      "id": "value",
      "title": "value",
      "isbn": "value",
      "isbn13": "value",
      "asin": "value",
      "kindle_asin": "value",
      "marketplace_id": "value",
      "country_code": "value",
      "image_url": "value",
      "small_image_url": "value",
      "publication_year": "value",
      "publication_month": "value",
      "publication_day": "value",
      "publisher": "value",
      "language_code": "value",
      "is_ebook": "value",
      "description": "value"
    }
  }
}
```
This json is what will be use as a format to extract data
Lets breakdown for each section, start with key "template", this key will contain a target element, and that element's child element. I call it target node
from this example, my target node is "book", if you look up at xml file, you will see that "book" have various child element, I write elements that I want as a member of "book" node in config.json

Now I will mention position of data and nested data, an element that also have a child simultaneously
xml have data contained in 2 positions, body of element or attribute of element
in case of body, I will define it as value
```dtd
<id>205330</id>
```
```
"id": "value"
```
when "id" element has value define as "value", my package will look for body of that element, and for attribute:
```dtd
<id key="205330"/>
```
```
"id":{
    "key": "attribute"
    }
```
as you noticed, I considered attribute as a nested data, because it can't be detected if not directly at that element.
the same goes for nested element, so I created nested element or element that I want attribute separately.
Now lets talke about those three
```
  "main_node": "book/similar_books/book",
  "sub_node": "book/similar_books/book/authors/author",
  "key_tag": "id",
```
if you're extracting data that doesn't require mapping, "main_node" is your target node, and you can replace "sub_node" and "key_tag" value by None.
but if it's need to be mapped, let's say that your target node is a child element of some element, and it's needed to be identify that this element belong to that parent,
put that parent node in "main_node", your target node in "sub_node", and element that use to mapped from main node in "key_tag"

### Usage
```
from xml_extractor.xml_extractor import XmlETExtractor

data = XmlETExtractor.xml_extractor(xml_template_path,config_path)
```
xml_template_path is a path of xml file, and config_path is a path of config.json
this process will return a class instance, the callable class attribute are
```
data.main_result
data.sub_result
```
it will return data that extract from main node and sub node accordingly, and there's callable function
```
data.main_result_to_parquet()
data.sub_result_to_parquet()
```
This function will write data to parquet file, path of the output os on const.py


