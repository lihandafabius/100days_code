import requests
from bs4 import BeautifulSoup

URL = "https://web.archive.org/web/20200518073855/https://www.empireonline.com/movies/features/best-movies-2/"

# Write your code below this line 👇
response = requests.get(URL)
data = response.text
soup = BeautifulSoup(data, "html.parser")
print(soup.title)
anchor_tags = soup.find_all(name="h3", class_="title")
print(anchor_tags)
reversed_anchor_tags = reversed(anchor_tags)
print(reversed_anchor_tags)
with open("movies.txt", mode="w", encoding="utf-8") as lists:
    for tag in reversed_anchor_tags:
        movie_title = tag.getText()
        print(movie_title)
        lists.write(movie_title + "\n")
