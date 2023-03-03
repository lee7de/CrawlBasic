def getHtml(url):
    import requests
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


def getHtmlEx(url):
    import sys
    import requests
    import chardet
    fakeHeaders = {'User-Agent':
                       'Mozilla/5.0 (Windows NT 10.0; Win64; x64)  \
                       AppleWebKit/537.36 (KHTML, like Gecko) \ '
                       'Chrome/81.0.4044.138 Safari/537.36 Edg/81.0.416.77',
                   'Accept': 'text/html,application/xhtml+xml,*/*'}
    try:
        r = requests.get(url, headers=fakeHeaders)
        ecd = chardet.detect(r.content)['encoding']
        if ecd.lower() != sys.getdefaultencoding().lower():
            r.encoding = ecd
        else:
            r.encoding = r.apparent_encoding
        return r.text
    except Exception as e:
        print(e)
        return ""


# print(getHtml("http://openjudge.cn"))
print(getHtml("https://www.baidu.com"))
