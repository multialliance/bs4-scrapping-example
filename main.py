# Import with pip bs4, requests, from bs4 import BeautifulSoup, import requests, import csv
from bs4 import BeautifulSoup
import requests
import csv

# Configure the csv file where elements finded wil be stored
filename = "libros_scrapper.csv"
columns = ["Item", "UPC", "Títle", "Price", "Image URL", "Description"]

with open(filename, "w", encoding='utf-8') as csvfile:
    writer = csv.writer(csvfile)
    writer.writerow(columns)

# Set the urls to scrape
urls = [
   "https://books.toscrape.com/catalogue/page-1.html",
   "https://books.toscrape.com/catalogue/page-2.html",
   "https://books.toscrape.com/catalogue/page-3.html"
   ]

urlbase = "https://books.toscrape.com/catalogue/" # Set the base url to add to the relatives urls finded

container = []
def soups(url):  # Function that Finds all "div" elements with the class "image_container" in the given url
   container.clear
   response = requests.get(url)   
   sopa = BeautifulSoup(response.content,'html.parser')
   container.append(sopa.find_all("div", class_="image_container"))

for url in urls: # run the soups function for each url
   soups(url)
container = container[0]+container[1]+container[2] # extract lists in a single list

item = 0
for link in container:  # find UPC, book title, price, url image and description
    if item < 50:
       item += 1
       url_book = link.find("a")["href"]
       url_book = urlbase+url_book
       bookresponse = requests.get(url_book)
       sopaf = BeautifulSoup(bookresponse.content,"html.parser")
       book_title = sopaf.find("h1")
       table = sopaf.find_all("tr")
       img_url_find = sopaf.find("div", class_="item active")
       img_url = img_url_find.find('img')['src']
       img_urlp = urlbase+img_url
       description = sopaf.select("#content_inner > article > p")
       datos = [item, table[0].find("td").text, book_title.text, table[3].find("td").text, img_urlp, description[0].text]

       with open(filename, "a", encoding='utf-8') as csvfile:
        writer = csv.writer(csvfile)
        writer.writerow(datos)
    else:
       break
