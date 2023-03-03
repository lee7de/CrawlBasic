import re
import requests

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

def getBaiduPictures(word, n):
    url = "https://image.baidu.com/search/index?tn=baiduimage&ipn=r&ct=201326592&cl=2&lm=-1&st=-1&fm=result&fr=&sf=1&fmq=1676865079901_R&pv=&ic=0&nc=1&z=&hd=&latest=&copyright=&se=1&showtab=0&fb=0&width=&height=&face=0&istype=2&dyTabStr=&ie=utf-8&sid=&word= "
    url += word
    html = getHtml(url)  # 用requests库获取网址url的网页
    pt = '\"thumbURL\":.*?\"(.*?)\"'
    i = 0
    for x in re.findall(pt, html):
        x = x.lower()
        print(x)
        # https://img0.baidu.com/it/u=3276999343,654799472&fm=253&fmt=auto&app=138&f=jpeg?w=500&h=667
        try:
            r = requests.get(x, stream=True)
            # print(r)
            f = open('{0}{1}.jpg'.format(word, i), "wb")
            f.write(r.content)
            f.close()
            i = i + 1
        except Exception as e:
            pass
        if i >= n:
            break


getBaiduPictures("music", 1)
