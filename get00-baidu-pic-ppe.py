import re
import requests


def getHtmlByPyppeteer(url):
    import asyncio  # 支持并行的协程库
    import pyppeteer as pyp
    async def asGetHtml(url):
        browser = await pyp.launch(headless=False)  # 无头模式容易被反爬，这里关掉
        page = await browser.newPage()
        await page.setUserAgent(
            'Mozilla/5.0 (Windows NT 6.1; Win64; \
            x64) AppleWebKit/537.36 (KHTML, like Gecko) \
            Chrome/78.0.3904.70 Safari/537.36')
        await page.evaluateOnNewDocument(
            '() =>{ Object.defineProperties(navigator, \
            { webdriver:{ get: () => false } }) }')
        await page.goto(url)
        text = await page.content()
        await browser.close()
        return text

    m = asyncio.ensure_future(asGetHtml(url))
    asyncio.get_event_loop().run_until_complete(m)  # 等待协程结束

    return m.result()



def getBaiduPictures(word, n):
    url = "https://image.baidu.com/search/index?tn=baiduimage&ipn=r&ct=201326592&cl=2&lm=-1&st=-1&fm=result&fr=&sf=1&fmq=1676865079901_R&pv=&ic=0&nc=1&z=&hd=&latest=&copyright=&se=1&showtab=0&fb=0&width=&height=&face=0&istype=2&dyTabStr=&ie=utf-8&sid=&word= "
    url += word
    html = getHtmlByPyppeteer(url)  # 用requests库获取网址url的网页
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


getBaiduPictures("装机", 5)
