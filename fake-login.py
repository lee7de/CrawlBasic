import asyncio
import pyppeteer as pyp


async def antiAntiCrawler(page):
    await page.setUserAgent('Mozilla/5.0 (Windows NT 6.1; \
		Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) \
    		Chrome/78.0.3904.70 Safari/537.36')
    await page.evaluateOnNewDocument(
        '() =>{ Object.defineProperties(navigator, \
        { webdriver:{ get: () => false } }) }')


async def getOjSourceCode(loginUrl):
    width, height = 1400, 800
    browser = await pyp.launch(headless=False,
                               userdataDir="c:/tmp",
                               args=[f'--window-size={width},{height}'])
    page = await browser.newPage()
    await antiAntiCrawler(page)
    await page.setViewport({'width': width, 'height': height})
    await page.goto(loginUrl)
    # 手动登录可去部分 begin
    # element = await page.querySelector("
    # await element.type("XXXXXXX@pku.edu.cn")
    # element = await page.querySelector("
    # await element.type("XXXXXXXXX")
    # element = await page.querySelector(
    #     "
    # await element.click()
    # await page.waitForSelector("
    # timeout = 30000)
    # element = await page.querySelector("
    #
    # await element.click()
    #
    # await page.waitForNavigation()
    # elements = await page.querySelectorAll(".result-right")
    #
    # page2 = await browser.newPage()
    # await antiAntiCrawler(page2)
    # for element in elements[:2]:
    #     obj = await element.getProperty("href")
    # url = await obj.jsonValue()
    # await page2.goto(url)
    # element = await page2.querySelector("pre")
    # obj = await element.getProperty("innerText")
    # text = await obj.jsonValue()
    # print(text)
    # print("-------------------------")
    # await browser.close()
    # 手动登录可去部分 end
    await page.waitForSelector("#main>h2",
                               timeout=30000)  # 等待“正在进行的比赛...."标题出现
    element = await page.querySelector("#userMenu>li:nth-child(2)>a")
    # 找"个人首页”链接
    await element.click()  # 点击个人首页链接
    await page.waitForNavigation()  # 等新网页装入完毕
    elements = await page.querySelectorAll(".result-right")
    # 找所有"Accepted"链接, 其有属性 class="result-right"
    page2 = await browser.newPage()  # 新开一个页面 (标签)
    await antiAntiCrawler(page2)
    for element in elements[:2]:  # 只打印前两个程序
        obj = await element.getProperty("href")  # 获取href属性
    url = await obj.jsonValue()
    await page2.goto(url)  # 在新页面(标签)中装入新网页
    element = await page2.querySelector("pre")  # 查找pre tag
    obj = await element.getProperty("innerText")  # 取源代码
    text = await obj.jsonValue()
    print(text)
    print("-------------------------")
    await browser.close()


def main():
    url = "http://openjudge.cn/auth/login/"
    asyncio.get_event_loop().run_until_complete(getOjSourceCode(url))

main()

