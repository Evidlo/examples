Source html

``` html
<html>
  <head>...</head>
  <body>
  <div id="topContainer">...</div>
  <div id="middleContainer" class="box">
    <div id="ctitle">Garbage Math</div>
    <ul class="comicNav">...</ul>
    <div id="comic">
      <img src="//imgs.xkcd.com/comics/garbage_math.png" title=...>
    </div>
    ...
```

Querying for `img` tag.  Returns html.Node

``` bash
>>> ./xpath -url "http://xkcd.com" -xpath "//div[@id='comic']/img"
&{0xc00036d7a0 <nil> <nil> 0xc00036d810 0xc00036d8f0 3 img img  [{ src //imgs.xkcd.com/comics/garbage_math.png} { title 'Garbage In, Garbage Out' should not be taken to imply any sort of conservation law limiting the amount of garbage produced.} { alt Garbage Math} { srcset //imgs.xkcd.com/comics/garbage_math_2x.png 2x}]}
```

Querying for `src` attribute of `img` tag.
``` bash
>>> ./xpath -url "http://xkcd.com" -xpath "//div[@id='comic']/img/@src"
&{<nil> 0xc0002d4c40 0xc0002d4c40 <nil> <nil> 3  src  []}
```

Python equivalent
``` python
>>> from lxml import html
>>> import requests
>>> r = requests.get('http://xkcd.com')
>>> h = html.fromstring(r.content)
>>> print(h.xpath('//div[@id="comic"]/img/@src'))
['//imgs.xkcd.com/comics/garbage_math.png']
```
