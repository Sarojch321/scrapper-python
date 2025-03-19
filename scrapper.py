import requests
from bs4 import BeautifulSoup
import json

URL = "https://books.toscrape.com/"

def scrape_books(url):
  response = requests.get(url)
  # print(response)
  # print(response.status_code)
  # print(response.text)
  if response.status_code != 200:
    print("Failed to fetch the page")
    return
  
  response.encoding = response.apparent_encoding
  
  soup = BeautifulSoup(response.text, "html.parser")
  books = soup.find_all("article", class_ = "product_pod")
  Lists = []
  for book in books:
    title = book.h3.a['title']  # tag. ma ani attributes ho vane [] vitra lekhne
    price_text = book.find("p", class_ = "price_color").text
    currency = price_text[0]
    price = price_text[1:]
    
    Lists.append({
        "title": title,
        "currency": currency,
        "price": price
    })

    with open("book_data.json", "w", encoding="utf-8") as f:
      json.dump(Lists, f, indent=4, ensure_ascii=False)

  print("Data is saved")


# read json and save in database


scrape_books(URL)