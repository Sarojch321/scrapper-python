import requests
from bs4 import BeautifulSoup
import json
import sqlite3

con = sqlite3.connect("book_data.sqlite3")
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

def read_json():
  books = []
  with open("book_data.json", "r", encoding="utf-8") as f:
    data = json.load(f)
    for book in data:
      books.append(tuple(book.values()))
  return books[1:]


def create_table(con):
  CREATE_TABLE = """
    CREATE TABLE IF NOT EXISTS books_data(
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    title CHAR(255) NOT NULL,
    currency CHAR(255) NOT NULL,
    price CHAR(255) NOT NULL
    );
    """
  cur = con.cursor()
  cur.execute(CREATE_TABLE)
  print("Books Data Table created successfully.")

def insert_book(con, books):
  INSERT_QUERY = """
    INSERT INTO books_data
    (
      title,
      currency,
      price
    )
    VALUES(?,?,?);
    """
  cur = con.cursor()
  cur.executemany(INSERT_QUERY, books)
  con.commit()
  print(f"{len(books)} books were inserted successfully.")


# read json and save in database

def main(url, con):
  scrape_books(url)
  print("Data is saved")

  books = read_json()

  create_table(con)

  insert_book(con, books)

  cur = con.cursor()
  

main(URL, con)


# install git
# create repositary in git
# go to bit bash
# git config --global user.name "Saroj Dangaura"
# git cinfig --global user.email "sarojdangaura321@gmail.com"
# git init
# git status => if you want to check what are the status of files
# git diff => if you want to check what are the changes
# git add .
# git commit -m "Your message"
# copy paste git code from github


# code change vayo vane jaile ni yo lekhne
# git add .   => track files and folders
# git commit -m "Your message"   => save changes
#git push  =>  uploads changes