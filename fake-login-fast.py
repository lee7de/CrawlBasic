import asyncio
import pyppeteer as pyp
import bs4
import requests

fakeHeaders = {'User-Agent':
                   'Mozilla/5.0 (Windows NT 10.0; Win64; x64)  \
                   AppleWebKit/537.36 (KHTML, like Gecko) \ '
                   'Chrome/81.0.4044.138 Safari/537.36 Edg/81.0.416.77'}


async def antiAntiCrawler(page):
    await page.setUserAgent('Mozilla/5.0 (Windows NT 6.1; \
		Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) \
    		Chrome/78.0.3904.70 Safari/537.36')
    await page.evaluateOnNewDocument(
        '() =>{ Object.defineProperties(navigator, \
        { webdriver:{ get: () => false } }) }')


def sessionGetHtml(session, url):
    try:
        result = session.get(url, headers=fakeHeaders)
        result.encoding = result.apparent_encoding
        return result.text
    except Exception as e:
        print(e)
        return ""


async def makeSession(page):
    cookies = await page.cookies()
    cookies1 = {}
    for cookie in cookies:
        cookies1[cookie['name']] = cookie['value']
    session = requests.Session()
    session.cookies.update(cookies1)
    return session


async def getOjSourceCode(loginUrl):
    width, height = 800, 600
    browser = await pyp.launch(headless=False,
                               userdataDir="c:/tmp",
                               args=[f'--window-size={width},{height}'])
    page = await browser.newPage()
    await antiAntiCrawler(page)
    await page.setViewport({'width': width, 'height': height})
    await page.goto(loginUrl)
    # await page.waitForSelector("
    # timeout = 30000)
    # element = await page.querySelector("
    #
    # await element.click()
    # await page.waitForNavigation()
    # elements = await page.querySelectorAll(".result-right")
    #
    # session = await makeSession(page)
    # for element in elements[:2]:
    #     obj = await element.getProperty("href")
    # url = await obj.jsonValue()
    # html = sessionGetHtml(session, url)
    # soup = bs4.BeautifulSoup(html, "html.parser")
    # element = soup.find("pre")
    # print(element.text)
    # print("-------------------------")
    # await browser.close()
    await page.waitForSelector("#main>h2",
                               timeout=30000)  # ??????????????????????????????...."????????????
    element = await page.querySelector("#userMenu>li:nth-child(2)>a")
    # ???"?????????????????????
    await element.click()  # ????????????????????????
    await page.waitForNavigation()  # ????????????????????????
    elements = await page.querySelectorAll(".result-right")
    # ?????????"Accepted"??????, ???????????? class="result-right"
    page2 = await browser.newPage()  # ?????????????????? (??????)
    await antiAntiCrawler(page2)
    for element in elements[:2]:  # ????????????????????????
        obj = await element.getProperty("href")  # ??????href??????
    url = await obj.jsonValue()
    await page2.goto(url)  # ????????????(??????)??????????????????
    element = await page2.querySelector("pre")  # ??????pre tag
    obj = await element.getProperty("innerText")  # ????????????
    text = await obj.jsonValue()
    print(text)
    print("-------------------------")
    await browser.close()

def main():
    url = "http://openjudge.cn/auth/login/"
    asyncio.get_event_loop().run_until_complete(getOjSourceCode(url))


main()