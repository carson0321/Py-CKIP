# Py-CKIP

Py-CKIP is a python API for CKIP Chinese Parser and Chinese Segmentator. The parser analyses the internal structure of Chinese words using [CKIP services](http://ckip.iis.sinica.edu.tw/CKIP/index.htm). CKIP(Chinese Knowledge and Information Processing Group) was invented by Taiwan Academia Sinica. In general, we can call through web services or crawl their websites to use. I found many implementations on the Internet, so I referred to the internet for implementations. There are two usages to provide. Please read the following instructions carefully.

Tested on

* Ubuntu 16.04.2 LTS Xenial Xerus (Python 2.7.12)

Tree:
```bash
├── __init__.py
├── PyCCP.py
├── PyCKIP.py
└── PyCSS.py
```

* **PyCKIP.py** is a simple interface for CKIP services. It provides two classes, `CKIPSegmenter` and `CKIPParser`, to access the [Chinese Segmenter](http://ckipsvr.iis.sinica.edu.tw/) and the [Chinese Parser](http://parser.iis.sinica.edu.tw/), respectively.

* **PyCCS.py** is a independent Python API for CKIP Chinese Segmentator. Because CKIP provides a online Chinese Segmentation tool, we can write a script that uses online tool to implement Chinese Segmentator using CKIP services.

* **PyCCP.py** is a independent Python API for CKIP Chinese Parser. CKIP provides a online Chinese Parser tool. Because CKIP provides a online Chinese Parsation tool, we can write a script that uses online tool to implement Chinese Parser by CKIP services.


## Requirements

```bash
pip install lxml 
```


## Usage 1: PyCKIP


To create an instance of these classes, you must import the `CKIPSegmenter` class and/or the `CKIPParser` class from the `ckip` module, and then pass your username and password to the constructor:

```python
from PyCKIP import *

segmenter = PyCKIP.CKIPSegmenter('YOUR USERNAME', 'YOUR PASSWORD')
parser = PyCKIP.CKIPParser('YOUR USERNAME', 'YOUR PASSWORD')
```

Then, you can use the `process()` method to process the given string:

```python
segmented_result = segmenter.process('這是一隻可愛的小花貓')
```

or

```python
parsed_result = parser.process('這是一隻可愛的小花貓')
```

This method returns a dictionary of the processed result:

```python
{
    'status': 'Success',
    'status_code': '0',
    'result':
        [
            [
                {'term': u'這', 'pos': u'DET'},
                {'term': u'是', 'pos': u'Vt'},
                {'term': u'一', 'pos': u'DET'},
                {'term': u'隻', 'pos': u'M'},
                {'term': u'可愛', 'pos': u'Vi'},
                {'term': u'的', 'pos': u'T'},
                {'term': u'小', 'pos': u'Vi'},
                {'term': u'花貓', 'pos': u'N'}
            ]
        ]
}
```

The `status` and the `status_code` indicate whether the process is success or not:

```python
if segmented_result['status_code'] != '0':
    print('Process Failed: ' + segmented_result['status'])
```

And the `result` is a list of objects that represent each sentence.

Takes the result of the `CKIPSegmenter.process()` for example, the sentence is represented by a list of dictionary. Each dictionary contains the Chinese term and the corresponding part-of-speech:

```python
for sentence in segmented_result['result']:
    for term in sentence:
        print(term['term'], term['pos'])
```

The sentence in the result of the `CKIPParser.process()`, on the other hand, is represented by a parsing tree:

```python
{
    'punctuation': None,
    'tree':
        {
            'head': {'term': u'是', 'pos': u'Vt'},
            'pos': u'S',
            'child':
                [
                    {
                        'head': {'term': u'這', 'pos': u'DET'},
                        'pos': u'NP',
                        'child':
                            [
                                {'term': u'這', 'pos': u'DET'}
                            ]
                    },
                    {'term': u'是', 'pos': u'Vt'},
                    {
                        'head': {'term': u'花貓', 'pos': u'N'},
                        'pos': u'NP',
                        'child':
                             [
                                 {'term': u'一隻', 'pos': u'DM'},
                                 {
                                     'head': {'term': u'的', 'pos': u'T'},
                                     'pos': u'V‧的',
                                     'child':
                                         [
                                             {'term': u'可愛', 'pos': u'Vi'},
                                             {'term': u'的', 'pos': u'T'}
                                         ]
                                 },
                                 {'term': u'小', 'pos': u'Vi'},
                                 {'term': u'花貓', 'pos': u'N'}
                             ]
                    }
                ]
        }
}
```

The `punctuation` is a dictionary like `{'term': u'。', 'pos': u'PERIODCATEGORY'}`, which represents the symbol that used to separate from next sentence, or `None` if there was no punctuation in this sentence.

`tree` is a dictionary that represent the tree structure. Each node has its own part-of-speech, and its children nodes (if this node is an internal node) or term (if this node is a leaf node).

Here is a simple example for traversing all leaf nodes (each of these is a Chinese term) of the parsing tree:

```python
def traverse(root):
    if 'child' in root:
        for child in root['child']:
            for leaf in traverse(child):
                yield leaf
    else:
        yield root

for sentence in parsed_result['result']:
    for term in traverse(sentence['tree']):
        print(term['term'], term['pos'])
```


## Usage 2: PyCCS & PyCCP

###PyCCS:

```python
>>> from PyCCS import ckip
>>> result = ckip.seg('台灣大學語言學研究所')
>>> print result.text()
台灣/Nc 大學/Nc 語言學/Na 研究所/Nc 
>>> result.raw
[(u'\u53f0\u7063', u'Nc'),
 (u'\u5927\u5b78', u'Nc'),
 (u'\u8a9e\u8a00\u5b78', u'Na'),
 (u'\u7814\u7a76\u6240', u'Nc')]
```

All html-like tags will be segmentated normally. At [CKIP Online Demo](http://sunlight.iis.sinica.edu.tw/uwextract/demo.htm), if you input strings containing html-like tag, the results might be weird.

For example:
```python
>>> print ckip.seg('<h1>這是html tag</h1>').text()
<h1>/FW 這/Nep 是/SHI html/FW tag</h1>/FW 
```

**Limitations:**
Input encoding should can only be **CP950/BIG5**. If words contains "堃" or "瑠", it will not be segmentated.

###PyCCP:

```python
from PyCCP import parseTree<br>
res = parseTree('蟹老闆好帥氣。')
```

License
-------

This software is licensed under the [MIT license](_MIT license: http://en.wikipedia.org/wiki/MIT_License).

```
MIT License

Copyright (c) 2016 Carson Wang <kiki86151@hotmail.com>

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
SOFTWARE.

```

© 2016 Carson Wang.