def getHtml(url):
    import asyncio
    import pyppeteer as pyp
    async def asGetHtml(url):
        browser = await pyp.launch(headless=False)

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
    asyncio.get_event_loop().run_until_complete(m)
    return m.result()


# print(getHtml("https://quote.eastmoney.com/sh600000.html"))
print(getHtml("https://www.bilibili.com/"))