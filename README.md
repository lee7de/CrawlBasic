# Crawl Basic

## 概述

数据获取型爬虫的基本逻辑

本质：自动获取网页内容并选择指定内容

步骤：

1. 页面下载，分析出对应`url`
2. 页面解析，通过解析获得获取指定的资源`url`
3. 数据存储，用文件或数据库将资源内容存储

## 前置知识

#TODO

## 例子：获取百度/必应/Google 图片的搜索结果

### 1 页面分析

百度搜索 `“chatgpt”`

```
https://image.baidu.com/search/index?tn=baiduimage&ipn=r&ct=201326592&cl=2&lm=-1&st=-1&fm=result&fr=&sf=1&fmq=1676865079901_R&pv=&ic=0&nc=1&z=&hd=&latest=&copyright=&se=1&showtab=0&fb=0&width=&height=&face=0&istype=2&dyTabStr=&ie=utf-8&sid=&word=chatgpt
```

观察链接构成，猜测搜索原理

https://image.baidu.com/search/index?tn=baiduimage&ipn=r&ct=201326592&cl=2&lm=-1&st=-1&fm=result&fr=&sf=1&fmq=1676865079901_R&pv=&ic=0&nc=1&z=&hd=&latest=&copyright=&se=1&showtab=0&fb=0&width=&height=&face=0&istype=2&dyTabStr=&ie=utf-8&sid=&word= **chatgpt**

验证猜想：

```
https://image.baidu.com/search/index?tn=baiduimage&ipn=r&ct=201326592&cl=2&lm=-1&st=-1&fm=result&fr=&sf=1&fmq=1676865079901_R&pv=&ic=0&nc=1&z=&hd=&latest=&copyright=&se=1&showtab=0&fb=0&width=&height=&face=0&istype=2&dyTabStr=&ie=utf-8&sid=&word=二次元
```

### 2 页面分析

复制图片链接发现规律

```
https://img1.baidu.com/it/u=2971608794,2256560419&fm=253&fmt=auto&app=138&f=JPG?w=500&h=281


https://img1.baidu.com/it/u=2192429849,3208186763&fm=253&fmt=auto&app=138&f=JPEG?w=701&h=500


https://image.baidu.com/search/detail?ct=503316480&z=&tn=baiduimagedetail&ipn=d&word=%E5%AD%A6%E7%94%9F&step_word=&ie=utf-8&in=&cl=2&lm=-1&st=-1&hd=&latest=&copyright=&cs=1499347630,3456351026&os=2193017757,2930546079&simid=1499347630,3456351026&pn=3&rn=1&di=7169026086108397569&ln=1980&fr=&fmq=1676865079901_R&ic=0&s=undefined&se=&sme=&tab=0&width=&height=&face=undefined&is=0,0&istype=2&ist=&jit=&bdtype=0&spn=0&pi=0&gsm=1e&objurl=https%3A%2F%2Fpicnew11.photophoto.cn%2F20170305%2Fgaoxingshangxuedeyiqunxueshengtupian-24753620_1.jpg&rpstart=0&rpnum=0&adpicid=0&nojc=undefined

https://img0.baidu.com/it/u=2311341614,4128563750&fm=253&fmt=auto&app=120&f=JPEG?w=1200&h=785

https://img0.baidu.com/it/u=2311341614,4128563750&fm=253&fmt=auto&app=120&f=JPEG?w=1200&h=785
```

结论：前缀相同，为百度保存缩略图的网址

通过上面的分析，我们可以：

1. 首先，分析需要爬取的页面的源代码`Ctrl+F`找到对应的地址标识；

![image-20230223102029703](CrawlBasic.assets/image-20230223102029703.png)

2. 然后就用正则表达式提取图片链接，批量寻找图片网址，同时考虑到有些图片爬取异常，加入try-except跳过去

* 导入必要的库

```python
import re
import requests
```

* 定义网页获取子函数

> ```
> 'Accept': 'text/html,application/xhtml+xml,*/*'
> ```
>
> 对付反爬

```python
def getHtml(url):
    fakeHeaders = {'User-Agent':
                       'Mozilla/5.0 (Windows NT 10.0; Win64; x64)  \
		   AppleWebKit/537.36 (KHTML, like Gecko) \ '
                       'Chrome/81.0.4044.138 Safari/537.36 Edg/81.0.416.77',
                   'Accept': 'text/html,application/xhtml+xml,*/*'
                   }
    try:
        r = requests.get(url, headers=fakeHeaders)
        r.encoding = r.apparent_encoding
        return r.text
    except Exception as e:
        print(e)
        return None
```

* 获取图片链接并保存

> `.*`:匹配任意不含“\n”的字符串，包括空串
>
> 加上`?`：尽可能短

```python
def getBaiduPictures(word, n):
    url = ""
    url += word
    html = getHtml(url)  # 用requests库获取网址url的网页
    pt = '\"thumbURL\":.*?\"(.*?)\"'
    i = 0
    for x in re.findall(pt, html):
        x = x.lower()
        print(x)
        try:
            r = requests.get(x, stream=True)
            f = open('{0}{1}.jpg'.format(word, i), "wb")
            f.write(r.content)
            f.close()
            i = i + 1
        except Exception as e:
            pass
        if i >= n:
            break
```

3. 调用函数，实现图片爬取

```python
getBaiduPictures("石头", 4)
```

# 1 页面下载

## `html`网页渲染概述

我们所访问的web页面对资源的加载大致分为返回一个静态的页面和动态生成互动页面两种方式。

> 一般地，在静态页面的处理上`requests`能满足大部分测试+抓取需求，动态页面用`pyppeteer`
>
> 进阶工程化`scrapy`，动态网页优先找`API接口`，如果有简单加密就破解，实在困难就使用`splash`渲染

静态页面：

* `requests`
* ~~`urllib`~~

动态生成页面：

* ~~selenium或~~`pyppeteer`
  * `pip install pyppeteer`
  * [使用`pyppeteer`手动下载chromium](https://cloud.tencent.com/developer/article/1731720)
* `Playwright`

## 动态页面类网页爬取原理

* 启动一个浏览器Chromium，用浏览器装入网页。浏览器可以用无头模式
  （headless)，即隐藏模式启动，也可以显式启动
* 从浏览器可以获取网页源代码，若网页有`javascript`程序，获取到的是
  `javascript`被浏览器执行后的网页源代码

## `pyppeteer`预备知识：协程

* 协程是一种特殊的函数，多个协程可以并行

* `pyppeteer中`的所有函数都是协程，调用时前面都要加 await，且协程只能在协程中调用

  * 协程编程有特殊的写法：

  * 对于`async def asGetHtml(url)`

  * ```python
    m = asyncio.ensure_future(asGetHtml(url))
    asyncio.get_event_loop().run_until_complete(m)
    ```

# 2 页面解析

* 通过`re`解析
* 通过`BeautifulSoup`或`lxml`

> 正则：速度快，多了就难记难学
>
> `BeautifulSoup`库：速度稍稍慢
>
> `pyppeteer`：速度慢代替复杂操作

## 网页结构

![DOM HTML tree](CrawlBasic.assets\ct_htmltree.gif)

![image-20230224111330724](CrawlBasic.assets/image-20230224111330724.png)



![image-20230224111354588](CrawlBasic.assets\image-20230224111354588.png)

```html
<a href="www.sohu.com" id='mylink'>搜狐网</a>
```

```html
<div id="siteHeader" class="wrapper">
    <h1 class="logo">
    <div id="topsearch">
        <ul id="userMenu">
        <li ><a href="http://openjudge.cn/">首页</a></li>
    </div>
</div>
```

## bs4分析过程

1. 将html文档装入一个`BeautifulSoup`对象X;

2) 用X对象的find,find_all等函数去找想要的tag对象;
3) 对找到的tag对象，还可以用其find,find_all函数去
   找它内部包含（嵌套）的tag对象;
4) tag对象的text就是该对象里的正文（text），tag对
   象也可以看作是一个字典，里面包含各种属性(attr)及其
   值。

## `pyppeteer+requests`快速爬虫

### cookie和session

* 登录成功后，服务器向浏览器发送一些身份标识数据，称为cookie，浏览器以后每次向服务器发送请求，都带上cookie，服务器就能知道请求来自前面那个登录的浏览器了。

* 服务器在内存为浏览器维护一个session，每个浏览器对应不同的session，里面存放着该浏览器的状态（比如一系列的填表等步骤已经进行到什么程度），不同的session有不同的session id，浏览器发送请求的时候，如果带上session id,服务器也能知道是哪个浏览器在请求。

* 在客户计算机上由cookie可以生成标识同一个浏览器的session

### `pyppeteer+requests`工作原理

- `pyppeteer`的浏览器的页面有cookies()函数可以获得cookie
- `requests.Session()`可以生成一个空`session`
- `session`的`cookies.update(cookies)`函数可以根据cookies生成相应
  session
- session的`get(url)`函数，可以向服务器发送带session的请求
- 获得cookie，生成相应session以后，爬取网页都用session的get函数进行
  (前提：网页不是javascript生成的。如果是，依然用pyppeteer的浏览器爬取）

# 3 数据存储

* 文件 txt文本
* csv文件
* 数据库：
  * sqlite3 （python自带）
  * MySQL
  * MongoDB

# 进阶方向

* 改进模拟型网页获取源代码，所有标签在一个page对象打开


# 资源链接

[html知识](https://developer.mozilla.org/zh-CN/docs/Learn/Getting_started_with_the_web)

[Python爬虫的两套解析方法和四种爬虫实现](https://developer.aliyun.com/article/629417)

[Python爬虫：常用的爬虫工具汇总](https://zhuanlan.zhihu.com/p/47792650)

[爬虫利器 Puppeteer 的一些最佳实践](https://zhuanlan.zhihu.com/p/66296309)

* [Playwright: 比 Puppeteer 更好用的浏览器自动化工具](https://zhuanlan.zhihu.com/p/347213089)

[爬虫-2.xpath解析和cookie，session](https://developer.aliyun.com/article/1098494?spm=a2c6h.12873639.article-detail.36.445d6f67JvujAv&scm=20140722.ID_community@@article@@1098494._.ID_community@@article@@1098494-OR_rec-V_1)
