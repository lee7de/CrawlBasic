import bs4

soup = bs4.BeautifulSoup(open("test.html",
                              encoding="utf-8"), "html.parser")

div = soup.find("div", attrs={"class": "df_div2"})
for x in div.children:
    if x.name != None and x.name != 'p':
        print("name of son =", x.name)
        if hasattr(x, "attrs"):
            print("attrs =", x.attrs)
print(div.parent.name, div.parent["id"])
for x in div.parents:
    print(x.name, end=",")
