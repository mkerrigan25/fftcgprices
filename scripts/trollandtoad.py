import requests
from bs4 import BeautifulSoup

def get_db():
    from pymongo import MongoClient
    client = MongoClient('localhost:27017')
    db = client.fftcg
    return db

def add_card(db, cardname, cardnum):
    db.cards.insert({"cardname" : cardname, "cardnum" : cardnum, "store" : "trollandtoad.com"})

db = get_db()
response = requests.get("http://www.trollandtoad.com/Force-of-Will-and-Other-CCGs/10283.html?orderBy=Alphabetical+A-Z&filterKeywords=&sois=Yes&minPrice=&maxPrice=&pageLimiter=10000&showImage=Yes")
html = response.text
soup = BeautifulSoup(html, 'html.parser')
divTag = soup.find_all(class_="cat_result_wrapper")

for tag in divTag:
	imgTag = tag.find(class_="cat_result_image_wrapper")
	title = imgTag.find('img')['alt']
	if len(title.split(" - ")) > 1:
		if "Foil" in title.split(" - ")[2]:
			print("This is a foil")
		else:	
			print(imgTag.find('img')['alt'])
			add_card(db, title.split(" - ")[0], title.split(" - ")[1])
			print(imgTag.find('a')['href'])
			print(imgTag.find('img')['src'])
			print(tag.find(class_="quantity_text").text)
			print(tag.find(class_="price_text").text)
		