# from bs4 import BeautifulSoup
# import requests
# response = requests.get("https://news.ycombinator.com/")
# yc_web_page = response.text
# soup = BeautifulSoup(yc_web_page, "html.parser")
# print(soup.title)
# anchor_tags = soup.find_all(name="a")
# print(anchor_tags)
#
#
# # from bs4 import BeautifulSoup
# # import requests
# #
# # response = requests.get("https://news.ycombinator.com/")
# # yc_web_page = response.text
# # soup = BeautifulSoup(yc_web_page, 'html.parser')
# #
# # article_titles = []
# # article_links = []
# # for article_tag in soup.find_all(name="span", class_="titleline"):
# #     article_titles.append(article_tag.getText())
# #     article_links.append(article_tag.find("a")["href"])
# #
# # article_upvotes = []
# # for article in soup.find_all(name="td", class_="subtext"):
# #     if article.span.find(class_="score") is None:
# #         article_upvotes.append(0)
# #     else:
# #         article_upvotes.append(int(article.span.find(class_="score").contents[0].split()[0]))
# #
# # max_points_index = article_upvotes.index(max(article_upvotes))
# # print(
# #     f"{article_titles[max_points_index]}, "
# #     f"{article_upvotes[max_points_index]} points, "
# #     f"available at: {article_links[max_points_index]}."
# # )
#
#
#
#
#
#
#
#
#
#
#
# # import lxml
# #
# # with open('website.html', encoding="utf-8") as file:
# #     data = file.read()
# # soup = BeautifulSoup(data, "lxml")
#
# # print(soup.title.string)
# # print(soup.prettify())
# # print(soup.a) prints only the first anchor tag
# # all_anchor_tags = soup.find_all(name="a")
# # print(all_anchor_tags)
# # for tag in all_anchor_tags:
#     # print(tag.getText())
#     # print(tag.get("href"))
#     # pass
#
# # heading = soup.find(name="h1", id="name")
# # print(heading.name)
# # heading3 = soup.find(name="h3", class_="heading")
# # print(heading3.text)
# # company_url = soup.select_one(selector="p a")
# # print(company_url)
# # name = soup.select_one(selector="#name")
# # print(name)
# # headings = soup.select(".heading")
# # print(headings)
import requests
from bs4 import BeautifulSoup
import csv

# URL of the Audible page to scrape (e.g., Best Sellers page)
url = "https://www.audible.com/search?keywords=bestsellers"

# Send a GET request to the webpage
headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.3'}
response = requests.get(url, headers=headers)

# Parse the HTML content using BeautifulSoup
soup = BeautifulSoup(response.content, 'html.parser')

# Find all book containers (adjust the class according to the actual HTML structure of the page)
book_list = soup.find_all('li', {'class': 'bc-list-item'})

# Open a CSV file to store the results
with open('audible_books.csv', 'w', newline='', encoding='utf-8') as csvfile:
    csvwriter = csv.writer(csvfile)
    # Write the header row
    csvwriter.writerow(['Title', 'Subtitle', 'Author', 'Length', 'Release Date', 'Language'])

    # Loop through each book container and extract data
    for book in book_list:
        try:
            # Extract Title
            title_tag = book.find('a', class_='bc-link bc-color-link')
            title = title_tag.get_text(strip=True) if title_tag else 'N/A'

            # Extract Subtitle
            subtitle_tag = book.find('li', class_='subtitle')
            subtitle = subtitle_tag.get_text(strip=True) if subtitle_tag else 'N/A'

            # Extract Author
            author_tag = book.find('li', class_='authorLabel')
            author = author_tag.get_text(strip=True).replace('By:', '').strip() if author_tag else 'N/A'

            # Extract Length
            length_tag = book.find('li', class_='runtimeLabel')
            length = length_tag.get_text(strip=True).replace('Length:', '').strip() if length_tag else 'N/A'

            # Extract Release Date
            release_date_tag = book.find('li', class_='releaseDateLabel')
            release_date = release_date_tag.get_text(strip=True).replace('Release date:', '').strip() if release_date_tag else 'N/A'

            # Extract Language
            language_tag = book.find('li', class_='languageLabel')
            language = language_tag.get_text(strip=True).replace('Language:', '').strip() if language_tag else 'N/A'

            # Write the data to the CSV file
            csvwriter.writerow([title, subtitle, author, length, release_date, language])
        except Exception as e:
            print(f"Error scraping data: {e}")

print("Scraping completed!")
