import requests
from bs4 import BeautifulSoup
import os
import string

directory = os.getcwd()
page_number = int(input())
user_input_type = input()

for i in range(1, page_number + 1):
    if f"Page_{i}" not in os.listdir(directory):
        os.mkdir(f"{directory}\Page_{i}")

for page in range(1, page_number + 1):
    os.chdir(f"{directory}\Page_{page}")
    url = f"https://www.nature.com/nature/articles?searchType=journalSearch&sort=PubDate&page={page}"
    url = requests.get(url, headers={'Accept-Language': 'en-US,en;q=0.5'})
    soup = BeautifulSoup(url.content, 'html.parser')
    if url.status_code:
        data_name = soup.find_all("article")
        for i in data_name:
            data_type = i.find("span", attrs={'data-test': 'article.type'}).text
            data_type = data_type.strip()
            if data_type == user_input_type:
                data_soup = i.find("a", attrs={'data-track-action': 'view article'})
                data_title = data_soup.text.strip()
                data_title = data_title.translate(str.maketrans(' ', '_', string.punctuation))
                data_hyperlink = data_soup.get("href")
                data_hyperlink = f"https://www.nature.com{data_hyperlink}"
                real_url = requests.get(data_hyperlink, headers={'Accept-Language': 'en-US,en;q=0.5'})
                real_soup = BeautifulSoup(real_url.content, 'html.parser')
                real_content = real_soup.find("div", class_='c-article-body')
                if real_content:
                    real_content = real_content.text.strip()
                else:
                    real_content = real_soup.find("div", class_='article-item__body')
                    real_content = real_content.text.strip()
                real_content_byte = real_content.encode()
                with open(f"{data_title}.txt", "wb") as f:
                    f.write(real_content_byte)
print("Saved all articles.")