
import json
import requests
from bs4 import BeautifulSoup
from pprint import pprint

# import hw8.connect as connect
from hw8.seeds import autors_add, quotes_add

BASE_URL = 'https://quotes.toscrape.com/'
# response = requests.get(BASE_URL)
# soup = BeautifulSoup(response.text, 'lxml')
all_quotes = []
all_authors = []
all_authors_urls = []


def pages_list():
    page_namber = 1
    pages = []
    page = True
    while page:
        pages_url = f'{BASE_URL}page/{page_namber}'
        response = requests.get(pages_url)
        soup = BeautifulSoup(response.text, 'lxml')
        page = soup.find_all("li", class_ = "next")
        page_namber +=1
        pages.append(pages_url)
    return pages


def quotes_list(url):
    result = []
    response = requests.get(url)
    soup = BeautifulSoup(response.text, 'lxml')
    divs = soup.find_all("div", class_ = "quote")
    for div in divs:
        dict_for_one = {}
        quote = div.find("span", class_ = "text").text
        author = div.find("small", class_ = "author").text
        tgs = div.find_all("a", class_ = "tag")
        tags = []
        for tag in tgs:
            tags.append(tag.text)
        dict_for_one = {"tags":tags, 
                        "author":author,
                        "quote":quote }
        result.append(dict_for_one)
    return result


def authors_urls(page):
    result = []
    response = requests.get(page)
    soup = BeautifulSoup(response.text, 'lxml')
    divs = soup.find_all("div", class_ = "quote")
    for div in divs:
        author_url = div.find("a")["href"]
        result.append(f"{BASE_URL}{author_url[1:]}")
    return result


def author_page(url:str):
    response = requests.get(url)
    soup = BeautifulSoup(response.text, 'lxml')
    description = soup.find("div", class_ = "author-description").text.replace("\n","")
    fullname = soup.find("h3", class_="author-title").text.replace("-"," ")
    born_date = soup.find("span", class_ = "author-born-date").text
    born_location = soup.find("span", class_="author-born-location").text
    dic = {
            "fullname": fullname,
            "born_date": born_date,
            "born_location": born_location,
            "description": description.strip()
        }
    return dic



if __name__ == '__main__':
    pages_list = pages_list()
    
    for page in pages_list:
        all_quotes.extend(quotes_list(page))
        all_authors_urls.extend(authors_urls(page))
        print("*")
    with open('quotes.json', 'w', encoding='utf-8') as fd:
        json.dump(all_quotes, fd, ensure_ascii=False, indent=4)

    all_authors_urls = set(all_authors_urls)
    for i in all_authors_urls:
        print(".")
        all_authors.append(author_page(i))
    with open('authors.json', 'w', encoding='utf-8') as fd:
        json.dump(all_authors, fd, ensure_ascii=False, indent=4)

    print("---adding authors to DB---")
    with open("authors.json", encoding='utf-8') as file:
        autors_add(json.load(file))

    print("---adding qoutes to DB---")
    with open("quotes.json", encoding='utf-8') as file:
        quotes_add(json.load(file))

    print("The end")






