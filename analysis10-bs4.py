import bs4

page_str = '''
<div id="siteHeader" class="wrapper">
	<h1 class="logo">
	<div id="topsearch">
		<ul id="userMenu">
		<li ><a href="http://openjudge.cn/" name='ok'>首页</a></li>
	</div>
</div>
'''

soup = bs4.BeautifulSoup(page_str, "html.parser")
tag = soup.find("li")
print("1: " + tag.text)

tag_a = soup.find("a")
print(f"2: {tag_a.name}")
print("3: " + tag_a.text)
print(f"4: {tag_a.attrs}")
print("5: " + tag_a["name"])
print("6: " + tag_a["href"])


