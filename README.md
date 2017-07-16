# Scrapy 入门

这是用 Scrapy 写的一个简单的爬虫，用来爬取今日头条的段子板块 [http://www.toutiao.com/ch/essay_joke/](http://www.toutiao.com/ch/essay_joke/)

版本：

Python 2.7.13
Scrapy 1.4.0

### 创建一个新项目

用下列命令创建一个项目

```bash
scrapy startproject joke_of_toutiao
```

此时的目录结构如下：

```bash
└── joke_of_toutiao
    ├── joke_of_toutiao
    │   ├── __init__.py
    │   ├── items.py
    │   ├── middlewares.py
    │   ├── pipelines.py
    │   ├── settings.py
    │   └── spiders
    │       └── __init__.py
    └── scrapy.cfg
```

### 第一个爬虫

用下列命令生成一个默认的 spider：

```bash
scrapy genspider joke http://www.toutiao.com/ch/essay_joke/
```

此时目录结构如下：

```bash
├── joke_of_toutiao
│   ├── __init__.py
│   ├── items.py
│   ├── middlewares.py
│   ├── pipelines.py
│   ├── settings.py
│   └── spiders
│       ├── __init__.py
│       └── joke.py
└── scrapy.cfg
```

注意在 spiders 目录下多了一个名为 `joke.py` 的文件，也可以不用 `genspider` 命令，
直接在 spiders 目录下写爬虫即可，用这个命令的好处是自动帮你生成了一些代码

有了这个整体结构后我们要做的就是在相应文件中填自己的代码了，大概的顺序如下：

1. joke.py 这个文件主要写网页解析相关的程序
2. items.py 定义数据模型，即要存的字段
3. pipelines.py 存储数据
4. settings.py 配置一些基本信息，比如请求头，开启哪些管道等

#### items.py

在这里定义字段，这里我们只定义一个字段，joke

```python
class JokeOfToutiaoItem(scrapy.Item):

    joke = scrapy.Field()
```

#### joke.py

解析网页，由于头条的信息是动态加载，需要分析浏览器请求，最后分析出来的链接形式
类似这样：`http://www.toutiao.com/api/article/feed/?category=essay_joke&utm_source=toutiao&widen=1&max_behot_time=0&max_behot_time_tmp=0&tadrequire=true&as=A12529565B53C57&cp=596B730C45272E1`，这个链接应该是与 session 相关的，后面的俩值
as= 与 cp= 应该是动态计算的。过一段时间应该就拿不到数据了，暂时不管这个，看代码
怎么写就行。具体程序见 joke.py，下面列出几个关键部分

- 引入 item

```python
from joke_of_toutiao.items import JokeOfToutiaoItem
```

- start\_urls 里写上要抓的链接

```python
start_urls = [
    http://www.toutiao.com/api/article/feed/?category=essay_joke&utm_source=toutiao&widen=1&max_behot_time=0&max_behot_time_tmp=0&tadrequire=true&as=A12529565B53C57&cp=596B730C45272E1,
]
```

- parse 里写解析部分的代码

response 参数代表请求返回的结果，这里有两点需要注意：

1. 如何产生 item -> 见 `yield joke_item` 相关部分代码
2. 如何重新发起请求 -> 见 `yield req` 相关部分代码

#### pipelines.py

在 joke.py 里 yield 的 joke\_item 最终会交给 pipelines 的类的 process\_item 方
法来处理，在这里我们简单的把 joke 存在文件里，实际可能会存数据库

#### settings.py

在这里配置基本信息，包括简单的 User-Agent 配置，开启 pipelines 等，需要注意的
是 pipelines 一定要被开启，否则 item 不会被处理，相应代码如下

```python
ITEM_PIPELINES = {
    'joke_of_toutiao.pipelines.JokeOfToutiaoPipeline': 300,
}
```

其它配置信息直接看代码吧

### 后记

其实用 scrapy 写爬虫的流程大概就是这样，真正难的是如何让爬虫不被识别出来，这个
爬虫应该很快就会被封的
