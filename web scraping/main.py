from bs4 import BeautifulSoup
import lxml

with open('website.html', encoding="utf-8") as file:
    data = file.read()
soup = BeautifulSoup(data, "lxml")

# print(soup.title.string)
# print(soup.prettify())
# print(soup.a) prints only the first anchor tag
all_anchor_tags = soup.find_all(name="a")
# print(all_anchor_tags)
for tag in all_anchor_tags:
    # print(tag.getText())
    # print(tag.get("href"))
    pass

# heading = soup.find(name="h1", id="name")
# print(heading.name)
# heading3 = soup.find(name="h3", class_="heading")
# print(heading3.text)
company_url = soup.select_one(selector="p a")
print(company_url)
name = soup.select_one(selector="#name")
print(name)
headings = soup.select(".heading")
print(headings)