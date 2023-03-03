import bs4

soup = bs4.BeautifulSoup(open("test.html",
                              encoding="utf-8"), "html.parser")
diva = soup.find("div", attrs={"id": "synoid"})

if diva != None:
    for x in diva.find_all("span", attrs={"class": "p1-4"}):
        print(x.text)

    for x in diva.find_all("a", attrs={"id": "searchlink1"}):
        print(x.text)

    x = diva.find("a", attrs={"id": "searchlink1", "class": "sh2"})
    if x != None:
        print(x.text)
        print(x["href"])
        print(x["id"])