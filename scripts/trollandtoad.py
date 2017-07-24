import requests
from bs4 import BeautifulSoup

def get_db():
    from pymongo import MongoClient
    client = MongoClient('mongodb://fftcgscript:nextat765@ds161022.mlab.com:61022/fftcg')
    db = client.fftcg
    return db

def add_card(db, cardname, cardnum):
    db.cards.update({"cardnum" : cardnum}, {"$set": {"cardname" : cardname, "cardnum" : cardnum, "store" : "trollandtoad.com"} }, upsert=True)

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
			#print(imgTag.find('img')['alt'])
			cardname, cardnum, rarity = title.split(" - ")
			if cardnum[-1].isdigit():
				print cardnum[-1]
				print rarity
				print rarity[0]
				cardnum = cardnum + rarity[0]
				print cardnum
			add_card(db, cardname, cardnum)
			#print(imgTag.find('a')['href'])
			#print(imgTag.find('img')['src'])
			#print(tag.find(class_="quantity_text").text)
			#print(tag.find(class_="price_text").text)
		